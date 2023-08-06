# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    zpipe_output_log.py
   Author :       Zhang Fan
   date：         2019/4/12
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

from zlogger import logger
from zlogger import logger_level

from zpipe import plugin_base
from zpipe import frame_config_path_join


class zpipe_output_log(plugin_base):
    __attrs__ = dict(
        log_name='zpipe_output_log',
        write_stream=True,
        write_file=False,
        file_dir='.',
        level='debug',
        interval=1,
        backupCount=2,
        info_level='info',
        log_inst=None,
    )

    def plugin_init(self, **kw):
        self.config = {k: kw[k] if k in kw else v for k, v in self.__attrs__.items()}

        self.config['name'] = self.config.pop('log_name')
        self.config['file_dir'] = frame_config_path_join(self.config['file_dir'])
        self.config['level'] = logger_level(self.config['level'].upper())

        self.info_level = self.config.pop('info_level')
        self.log_inst = self.config.pop('log_inst')
        if not self.log_inst:
            self.log_inst = logger(**self.config)

    def process(self, data):
        info_level = self.extract_data(data, self.info_level, 'info')
        func = getattr(self.log_inst, info_level.lower())
        func(str(data))
        return True
