# -*- coding: utf-8 -*-
"""
author: shanzha
WeChat: shanzhan09
create_time: 2021/04/27 14:14
"""

import os
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from COIPS.config import base_dir, batch_size, project_name, img_size
from tqdm import tqdm
from COIPS.utils import maybe_mkdir
import shutil

test_dir = os.path.join(base_dir, 'processed_OCTA_images')
device = torch.device("cuda:0")

report_dir = os.path.join(base_dir, 'report')
quality_assessment_dir = os.path.join(base_dir, 'quality_assessment')
ungradable_dir = os.path.join(quality_assessment_dir, 'ungradable')
gradable_dir = os.path.join(quality_assessment_dir, 'gradable')
outstanding_dir = os.path.join(quality_assessment_dir, 'outstanding')
maybe_mkdir(report_dir)
maybe_mkdir(quality_assessment_dir)
maybe_mkdir(ungradable_dir)
maybe_mkdir(gradable_dir)
maybe_mkdir(outstanding_dir)


def inference(logger, size=None):
    assert size in [3, 6]
    if size == 3:
        model = torch.load('../models/quality_assessment/seresnext101_3x3_all.pth')
    else:
        model = torch.load('../models/quality_assessment/seresnext101_6x6_all.pth')
    model.to(device)
    logger.info('Model loads success!!!')
    data_transform = {"inference": transforms.Compose([transforms.Resize(224),
                                                       transforms.ToTensor(),
                                                       transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
                      }
    test_dataset = datasets.ImageFolder(root=test_dir, transform=data_transform["inference"])
    test_dict = test_dataset.imgs
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    model.eval()
    Pred = []

    with torch.no_grad():
        for batch_index, (x, label) in tqdm(enumerate(test_loader)):
            x, label = x.to(device), label.to(device)

            logits = model(x)
            pred = logits.argmax(dim=1)

            pred = pred.detach().cpu().tolist()

            Pred.extend(pred)

    for x in zip(test_dict, Pred):
        with open('{}/{}_quality_assessment.csv'.format(report_dir, project_name), 'a+') as f:
            x = str(x).replace('\'', '').split(',')
            x = str(x[0]).replace('((', '') + ',' + str(x[2]).replace(')', '') + '\n'
            f.write(x)

    logger.info('COIPS quality assessment report generate done!!!')


def move_to_assessment_folder():
    """move each image to the folder, relatively"""
    with open('{}/{}_quality_assessment.csv'.format(report_dir, project_name), 'r') as f:
        data = f.read().split('\n')
        for item in data:
            if item:
                item_ = item.split(',')
                origin_path = item_[0]
                label = int(item_[1])
                name = origin_path.split('/')[-1]
                if label == 0:
                    target_path = os.path.join(ungradable_dir, name)
                elif label == 1:
                    target_path = os.path.join(gradable_dir, name)
                else:
                    target_path = os.path.join(outstanding_dir, name)
                shutil.copy(origin_path, target_path)


def main(logger):
    """
    This program assess the images in 'processed_OCTA_images' and move the images into subfolders 'ungradable',
     'gradale' and 'outstanding' in 'quality_assessment'
    """
    if os.path.exists(test_dir):
        inference(logger, size=img_size)
        move_to_assessment_folder()
        logger.info('COIPS quality assessment done!!!')
