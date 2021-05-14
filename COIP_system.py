# -*- coding: utf-8 -*-
"""
author: shanzha
WeChat: shanzhan09
create_time: 2021/05/14 13:22
"""
from COIPS import pre_processing, quality_assessment, FAZ_segmentation, segmentation_processing, visualization_and_report
from utils import logger_create

logger = logger_create()

if __name__ == '__main__':
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

# logger = logger_create()
# logger.info('CIOPS start...')
# logger.info('CIOPS pre_processing start...')
# pre_processing.main()
# logger.info('CIOPS quality assessment start...')
# quality_assessment.main()
# logger.info('CIOPS FAZ segmentation pre_processing start...')
# segmentation_processing.main()
# logger.info('CIOPS FAZ segmentation start...')
# FAZ_segmentation.FAZ_segmentation()
# logger.info('CIOPS visualization and report start...')
# visualization_and_report.main()
# logger.info('CIOPS run successfully!!!')