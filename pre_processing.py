# -*- coding: utf-8 -*-
import cv2
from COIPS.utils import subFiles, maybe_mkdir
from COIPS.config import base_dir
import shutil
import os
from tqdm import tqdm

raw_png_folder = os.path.join(base_dir, 'raw_OCTA_images')
processed_png_folder = os.path.join(base_dir, 'processed_OCTA_images')
processed_png_folder0 = os.path.join(processed_png_folder, '0')
maybe_mkdir(processed_png_folder)
maybe_mkdir(processed_png_folder0)

pic_type = ['.jpg', '.tif', 'jpeg']


def convert(img_path, obj_type, target_dir):
    """
    convert image format
    :param obj_type:
    :param img_path:
    :param target_dir:
    :return:
    """
    img = cv2.imread(img_path)
    name = img_path.split('/')[-1].split('.')[0]
    target_path = os.path.join(target_dir, '{}.{}'.format(name, obj_type))
    cv2.imwrite(target_path, img)


def main(logger):
    """
    This program will convert the other format OCTA images into .png, so please put all raw OCTA images at the base_dir
    you defined and rename the folder into  'raw_OCTA_images'
    """
    for type_ in pic_type:
        pic_list = subFiles(folder=raw_png_folder, suffix=type_)
        for pic in tqdm(pic_list):
            convert(img_path=pic, obj_type='png', target_dir=raw_png_folder)
    logger.info('All of images the format convert done!!!')
    png_list = subFiles(folder=raw_png_folder, suffix='.png')
    for pic in png_list:
        name = pic.split('/')[-1]
        target = os.path.join(processed_png_folder0, name)
        shutil.move(pic, target)
    logger.info('COIPS pre-processing done!!')
