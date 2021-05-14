import os
import torch
from nnunet.inference.predict import preprocess_multithreaded, check_input_folder_and_return_caseIDs
from nnunet.inference.segmentation_export import save_segmentation_nifti_from_softmax
from nnunet.training.model_restore import load_model_and_checkpoint_files
from COIPS.utils import subfilename, join, load_pickle, maybe_mkdir, isfile
from multiprocessing import Pool
import numpy as np
from COIPS.config import overwrite_existing, pool_num


model = '/media/wyf/dl/eye/final_project/models/FAZ_segmentation'
input_folder = '/media/wyf/dl/eye/final_project/FAZ_segmentation/gradable/predict_nii'
output_folder = '/media/wyf/dl/eye/final_project/FAZ_segmentation/gradable/predict_label'
output_filename = '/media/wyf/dl/eye/final_project/FAZ_segmentation/gradable/predict_label'

folds = (0, 1, 2, 3, 4)


def FAZ_segmentation(logger):
    """"""
    logger.info("emptying cuda cache")
    torch.cuda.empty_cache()
    expected_num_modalities = load_pickle(join(model, "plans.pkl"))['num_modalities']
    logger.info(expected_num_modalities)
    case_ids = check_input_folder_and_return_caseIDs(input_folder, expected_num_modalities)
    output_files = [join(output_folder, i + ".nii.gz") for i in case_ids]
    all_files = subfilename(input_folder, suffix=".nii.gz", join=False, sort=True)
    list_of_lists = [[join(input_folder, i) for i in all_files if i[:len(j)].startswith(j) and
                      len(i) == (len(j) + 12)] for j in case_ids]

    # predict_cases
    list_of_lists = list_of_lists[0::1]
    output_filenames = output_files[0::1]
    # print(list_of_lists, output_filenames)

    pool = Pool(pool_num)
    results = []
    cleaned_output_files = []
    for o in output_filenames:
        dr, f = os.path.split(o)
        if len(dr) > 0:
            maybe_mkdir(dr)
        if not f.endswith(".nii.gz"):
            f, _ = os.path.splitext(f)
            f = f + ".nii.gz"
        cleaned_output_files.append(join(dr, f))

    save_npz = False

    if not overwrite_existing:
        logger.info("number of cases: {}".format(len(list_of_lists)))
        # if save_npz=True then we should also check for missing npz files
        not_done_idx = [i for i, j in enumerate(cleaned_output_files) if
                        (not isfile(j)) or (save_npz and not isfile(j[:-7] + '.npz'))]

        cleaned_output_files = [cleaned_output_files[i] for i in not_done_idx]
        list_of_lists = [list_of_lists[i] for i in not_done_idx]

        logger.info("number of cases that still need to be predicted: {}".format(len(cleaned_output_files)))

    trainer, params = load_model_and_checkpoint_files(model, folds, mixed_precision=None, checkpoint_name='model_best')

    if 'segmentation_export_params' in trainer.plans.keys():
        force_separate_z = trainer.plans['segmentation_export_params']['force_separate_z']
        interpolation_order = trainer.plans['segmentation_export_params']['interpolation_order']
        interpolation_order_z = trainer.plans['segmentation_export_params']['interpolation_order_z']
    else:
        force_separate_z = None
        interpolation_order = 1
        interpolation_order_z = 0

    logger.info("starting preprocessing generator")
    preprocessing = preprocess_multithreaded(trainer, list_of_lists, cleaned_output_files, num_processes=4,
                                             segs_from_prev_stage=None)

    logger.info("starting prediction...")
    all_output_files = []
    for preprocessed in preprocessing:
        output_filename, (d, dct) = preprocessed
        all_output_files.append(all_output_files)
        if isinstance(d, str):
            data = np.load(d)
            os.remove(d)
            d = data

        logger.info("predicting {}".format(output_filename))
        softmax = []
        for p in params:
            trainer.load_checkpoint_ram(p, False)
            softmax.append(trainer.predict_preprocessed_data_return_seg_and_softmax(d, do_mirroring=True,
                                                                                    mirror_axes=trainer.data_aug_params[
                                                                                        'mirror_axes'],
                                                                                    use_sliding_window=True,
                                                                                    step_size=0.5, use_gaussian=True,
                                                                                    all_in_gpu=False,
                                                                                    mixed_precision=True)[1][None])

        softmax = np.vstack(softmax)
        softmax_mean = np.mean(softmax, 0)

        transpose_forward = trainer.plans.get('transpose_forward')
        if transpose_forward is not None:
            transpose_backward = trainer.plans.get('transpose_backward')
            softmax_mean = softmax_mean.transpose([0] + [i + 1 for i in transpose_backward])

        if save_npz:
            npz_file = output_filename[:-7] + ".npz"
        else:
            npz_file = None

        if hasattr(trainer, 'regions_class_order'):
            region_class_order = trainer.regions_class_order
        else:
            region_class_order = None
        bytes_per_voxel = 4
        if np.prod(softmax_mean.shape) > (2e9 / bytes_per_voxel * 0.85):  # * 0.85 just to be save
            logger.info(
                "This output is too large for python process-process communication. Saving output temporarily to disk")
            np.save(output_filename[:-7] + ".npy", softmax_mean)
            softmax_mean = output_filename[:-7] + ".npy"

        results.append(pool.starmap_async(save_segmentation_nifti_from_softmax,
                                          ((softmax_mean, output_filename, dct, interpolation_order, region_class_order,
                                            None, None,
                                            npz_file, None, force_separate_z, interpolation_order_z),)
                                          ))

        logger.info("inference done. Now waiting for the segmentation export to finish...")
        _ = [i.get() for i in results]

    pool.close()
    pool.join()
    logger.info('CIOPS FAZ segmentation done!!!')
