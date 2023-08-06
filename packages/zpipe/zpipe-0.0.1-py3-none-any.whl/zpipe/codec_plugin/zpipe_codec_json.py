# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    zpipe_codec_json.py
   Author :       Zhang Fan
   date：         2019/4/12
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import json

from zpipe import plugin_base


class zpipe_codec_json(plugin_base):
    def plugin_init(self, **kw):
        self.config = kw

    def process(self, data):
        result = json.loads(data.pop('raw'), **self.config)
        data.update(result)
        return data
