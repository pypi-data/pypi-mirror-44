# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    pipe_server.py
   Author :       Zhang Fan
   date：         2019/4/11
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import os
import sys
import json

from zpipe import frame_config_file
from zpipe import frame_config_path_join
from zpipe.pipe import pipe
from zpipe import pipe_exception


class pipe_server():
    _builtin_plugin_path = [
        './codec_plugin',
        './filter_plugin',
        './output_plugin',
    ]

    def __init__(self):
        self._base_path = os.path.abspath(os.path.dirname(__file__))

        assert os.path.isfile(frame_config_file), f'配置文件不存在:{frame_config_file}'
        self._config = self._load_config(frame_config_file)

        self._pipe_config = self._load_pipe_config()
        self._load_plugin_pack()

    def _base_join(self, path):
        return os.path.abspath(os.path.join(self._base_path, path))

    def _load_config(self, config_file) -> dict:
        config_text = open(config_file, 'r', encoding='utf8').read()
        return json.loads(config_text)

    def _load_pipe_config(self) -> dict:
        config = dict()
        pipe_pack_path = self._config.get('pipe_config_path') or ''
        for path in pipe_pack_path.split(';'):
            if not path:
                continue

            full_path = frame_config_path_join(path)
            if os.path.isfile(full_path):
                file_list = [full_path]
            elif os.path.isdir(full_path):
                file_list = [os.path.abspath(os.path.join(full_path, file)) for file in os.listdir(full_path)]
            else:
                file_list = []

            for file in file_list:
                try:
                    mapp = self._load_config(file)
                except:
                    raise Exception(f'无法加载配置文件<{file}>')
                config.update(mapp)
        return config

    def _load_plugin_pack(self):
        for path in self._builtin_plugin_path:
            sys.path.append(self._base_join(path))

        pipe_pack_path = self._config.get('plugin_path') or ''
        for path in pipe_pack_path.split(';'):
            if not path:
                continue

            path = frame_config_path_join(path)
            if os.path.isdir(path):
                sys.path.append(path)

    def get_pipe(self, name, **kw):
        try:
            config = self._pipe_config[name]
        except:
            raise pipe_exception(f'无法找到管道<{name}>')

        kw.update(config)
        return pipe(name, **kw)
