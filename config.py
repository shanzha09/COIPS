# -*- coding: utf-8 -*-
# raw OCTA images dir must be named "raw_OCTA_images"
# project base dir, where the 'raw_OCTA_images' is
base_dir = ''
# models dir
model_dir = './models_dict'
# batch size
batch_size = 32
# name of the project
project_name = '6x6'
# image size: 3 (means 3 x 3) or 6 (means 6 x 6)
img_size = 6
# vascular layer (superficial: 0 or deep: 1)
vascular_layer = 0
# if overwrite the segmentation results when you rerun the program
overwrite_existing = False
# multiprocessing pools
pool_num = 4
