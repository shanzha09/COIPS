# -*- coding: utf-8 -*-
import os
import pickle
import sys
import logging
from termcolor import colored
from COIPS.config import base_dir


def subFiles(folder, prefix=None, suffix=None, subdir=False):
    """
      get all the files in the folder
      :param
          folder: absolute path
          prefix:
          suffix:
          subdir: if there are sub folders in the path given
      :return
          list contain the files absolute path
      """
    _res = []
    for _i in os.listdir(folder):
        _file_path = os.path.join(folder, _i)
        if prefix and _i.startswith(prefix):
            if os.path.isfile(_file_path):
                _res.append(_file_path)
        if suffix and _i.endswith(suffix):
            if os.path.isfile(_file_path):
                _res.append(_file_path)
    if subdir:
        for _dirpath, _dirnames, _filenames in os.walk(folder):
            for _i in _filenames:
                _file_path = os.path.join(_dirpath, _i)
                if prefix and _i.startswith(prefix):
                    if os.path.isfile(_file_path):
                        _res.append(_file_path)
                if suffix and _i.endswith(suffix):
                    if os.path.isfile(_file_path):
                        _res.append(_file_path)
    return _res


def maybe_mkdir(path):
    """
    create the folder if it is not exited!
    :param path: absolute path of the folder
    :return:
    """
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)


def subfilename(folder, join=False, prefix=None, suffix=None, sort=True):
    if join:
        l = os.path.join
    else:
        l = lambda x, y: y
    res = [l(folder, i) for i in os.listdir(folder) if os.path.isfile(os.path.join(folder, i))
           and (prefix is None or i.startswith(prefix))
           and (suffix is None or i.endswith(suffix))]
    if sort:
        res.sort()
    return res


join = os.path.join
isfile = os.path.isfile


def load_pickle(file, mode='rb'):
    with open(file, mode) as f:
        a = pickle.load(f)
    return a


def logger_create():
    """create the logger"""
    logger = logging.getLogger(name='COIPS')
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    format_ = '[%(asctime)s %(name)s] (%(filename)s %(lineno)d): %(levelname)s %(message)s'
    color_format_ = colored('[%(asctime)s %(name)s]', 'yellow') + \
                colored('(%(filename)s %(lineno)d)', 'red') + ': %(levelname)s %(message)s'

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(
                    logging.Formatter(fmt=color_format_, datefmt='%Y-%m-%d %H:%M:%S'))
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(os.path.join(base_dir, f'COIPS_log.txt'), mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(fmt=format_, datefmt='%Y-%m-%d %H:%M:%S'))
    logger.addHandler(file_handler)
    return logger

