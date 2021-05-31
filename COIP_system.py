# -*- coding: utf-8 -*-
from COIPS import pre_processing, quality_assessment, FAZ_segmentation, segmentation_processing, visualization_and_report
from utils import logger_create
from COIPS.config import vascular_layer, img_size

logger = logger_create()

if __name__ == '__main__':
    assert img_size in [3, 6]
    assert vascular_layer in [0, 1]
    logger.info('CIOPS start...')
    logger.info('CIOPS pre_processing start...')
    pre_processing.main(logger)
    logger.info('CIOPS quality assessment start...')
    quality_assessment.main(logger)
    logger.info('CIOPS FAZ segmentation pre_processing start...')
    segmentation_processing.main(logger)
    logger.info('CIOPS FAZ segmentation start...')
    FAZ_segmentation.FAZ_segmentation(logger)
    logger.info('CIOPS visualization and report start...')
    visualization_and_report.main(logger)
    logger.info('CIOPS run successfully!!!')
