# -*- coding: utf-8 -*-
"""
author: shanzha
WeChat: shanzhan09
create_time: 2021/04/27 20:59
"""
import collections
import SimpleITK as sitk
from PIL import Image
import numpy as np
import cv2
from COIPS.utils import maybe_mkdir, subfilename, subFiles
import os
from tqdm import tqdm
from COIPS.config import base_dir, project_name


csv_path = os.path.join(base_dir, 'report')


def raw_pic_convert(path):
    """
    convert RGB to RGBA and return the pic
    :param path:
    :return:
    """
    pic = Image.open(path)
    pic = pic.convert('RGBA')
    return pic


def convert_nii_to_png(path):
    """
    convert .nii.gz label to png RGBA label mask and return
    :param path:
    :return:
    """
    raw_label = sitk.ReadImage(path)
    mask = sitk.GetArrayFromImage(raw_label)[0]
    for i in np.nditer(mask, op_flags=['readwrite']):
        i[...] = i * 255
    g, b = np.zeros(mask.shape[:2], dtype='uint8'), np.zeros(mask.shape[:2], dtype='uint8')
    mask = cv2.merge((mask, g, b))
    mask = Image.fromarray(mask)
    mask = mask.convert('RGBA')
    return mask


def get_nii(path):
    """
    convert .nii.gz label to png RGBA label mask and return
    :param path:
    :return:
    """
    raw_label = sitk.ReadImage(path)
    mask = sitk.GetArrayFromImage(raw_label)[0]
    x, y = mask.shape
    assert x == y
    assert len(mask.shape) == 2
    mask_pixel = mask.flatten()
    mask_pixel_num = dict(collections.Counter(mask_pixel)).get(1)
    return x, mask_pixel_num


def calculate_area(true_edge_length, edge_pixel, pixel_num):
    """
    calculate mask true area
    :param true_edge_length: true edge length i.e. mm, cm, m
    :param edge_pixel: pixel length of the image i.e. 320 x 320
    :param pixel_num: mask pixel number
    :return: true area
    """
    if pixel_num is None:
        pixel_num = 0
    area_per_pixel = float((true_edge_length ** 2) / (edge_pixel ** 2))
    area = area_per_pixel * pixel_num
    return area


def mask_convert():
    for i in ['gradable', 'outstanding']:
        raw_pic_dir = os.path.join(base_dir, 'quality_assessment', '{}'.format(i))
        nii_label_dir = os.path.join(base_dir, 'FAZ_segmentation', '{}'.format(i), 'predict_label')
        mask_dir = os.path.join(base_dir, 'FAZ_segmentation', '{}'.format(i), 'label_mask')
        source_images = subfilename(raw_pic_dir, join=False, suffix='png')
        maybe_mkdir(mask_dir)
        for i in tqdm(source_images):
            name = i.split('.')[0]
            pic_path = os.path.join(raw_pic_dir, i)
            nii_path = os.path.join(nii_label_dir, '{}.nii.gz'.format(name))
            if os.path.isfile(nii_path):
                # print(pic_path, nii_path)
                pic = raw_pic_convert(path=pic_path)
                mask = convert_nii_to_png(path=nii_path)
                label_mask = Image.blend(pic, mask, 0.15)
                label_mask.save(os.path.join(mask_dir, 'mask_{}.png'.format(name)))


def report():
    for i in ['gradable', 'outstanding']:
        nii_label_dir = os.path.join(base_dir, 'FAZ_segmentation', '{}'.format(i), 'predict_label')
        raw_nii_list = subFiles(nii_label_dir, suffix='.nii.gz')
        for j in tqdm(raw_nii_list):
            name = j.split('/')[-1].split('.')[0]
            x, mask_pixel_num = get_nii(path=j)
            area = calculate_area(3, x, mask_pixel_num)
            cache = name + ',' + str(area) + '\n'
            with open('{}/{}_FAZ_area_{}.csv'.format(csv_path, project_name, i), 'a+') as f:
                f.write(cache)


def main(logger):
    logger.info('mask converting...')
    mask_convert()
    logger.info('mask done!!')
    logger.info('reporting...')
    report()
    logger.info('reports generate done!!!')
