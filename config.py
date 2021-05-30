# -*- coding: utf-8 -*-
"""
author: shanzha
WeChat: shanzhan09
create_time: 2021/04/27 13:37
"""
# project base dir
base_dir = '/media/wyf/dl/批量FAZ测量/黄斑6_6mm/Input/deep'
model_dir = '/media/wyf/dl/eye/final_project/models_dict'
# batch size
batch_size = 32
# name of the project
project_name = '6x6'
# image size: 3x3 or 6x6
img_size = 6
# vascular layer (superficial: 0 or deep: 1)
vascular_layer = 1
# if overwrite the segmentation results when you rerun the program
overwrite_existing = False
# multiprocessing pools
pool_num = 4
