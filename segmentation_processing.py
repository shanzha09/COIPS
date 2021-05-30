# -*- coding: utf-8 -*-
"""
author: shanzha
WeChat: shanzhan09
create_time: 2021/04/27 16:02
"""

from nnunet.utilities.file_conversions import convert_2d_image_to_nifti
from COIPS.config import base_dir
from COIPS.utils import maybe_mkdir, subFiles
import os

for i in ['gradable', 'outstanding']:
    FAZ_segmentation_dir = os.path.join(base_dir, 'FAZ_segmentation')
    seg_dir = os.path.join(FAZ_segmentation_dir, '{}'.format(i))
    seg_nii_dir = os.path.join(seg_dir, 'predict_nii')
    seg_predict_label_dir = os.path.join(seg_dir, 'predict_label')
    seg_label_mask_dir = os.path.join(seg_dir, 'label_mask')
    maybe_mkdir(FAZ_segmentation_dir)
    maybe_mkdir(seg_dir)
    maybe_mkdir(seg_nii_dir)
    maybe_mkdir(seg_predict_label_dir)
    maybe_mkdir(seg_label_mask_dir)


def main(logger):
    """Convert all 'gradable' and 'outstanding'  images to .nii.gz"""
    for _i in ['gradable', 'outstanding']:
        FAZ_segmentation_dir = os.path.join(base_dir, 'FAZ_segmentation')
        seg_dir = os.path.join(FAZ_segmentation_dir, '{}'.format(_i))
        seg_nii_dir = os.path.join(seg_dir, 'predict_nii')

        input_OCTA_images_dir = os.path.join(base_dir, 'quality_assessment', '{}'.format(_i))
        input_OCTA_images_list = subFiles(folder=input_OCTA_images_dir, suffix='.png')

        for path in input_OCTA_images_list:
            name = path.split('/')[-1].split('.')[0]

            convert_2d_image_to_nifti(path, os.path.join(seg_nii_dir, name))

    logger.info('CIOPS FAZ segmentation pre_processing done!!!')
