# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    __init__.py.py
   Author :       Zhang Fan
   date：         2019/4/11
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import os
import sys


def _get_frame_config_file():
    file = os.getenv('ZPIPE_CONFIG')
    if file:
        return file
    if 'win' in sys.platform.lower():
        return 'c:/zpipe/config.json'
    return '/etc/zpipe/config.json'


def frame_config_path_join(path):
    return os.path.abspath(os.path.join(_frame_config_path, path))


frame_config_file = _get_frame_config_file()
_frame_config_path = os.path.abspath(os.path.dirname(frame_config_file))

from .exception import pipe_exception
from .exception import codec_exception
from .exception import filter_exception
from .exception import output_exception
from .plugin_base import plugin_base
from .pipe_server import pipe_server
