# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    zpipe_codec_msgpack.py
   Author :       Zhang Fan
   date：         2019/4/12
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import msgpack

from zpipe import plugin_base


class zpipe_codec_msgpack(plugin_base):
    def plugin_init(self, **kw):
        self.config = kw

    def process(self, data):
        result = msgpack.loads(data.pop('raw'), **self.config)
        if not isinstance(result, dict):
            result = dict(raw=result)
        data.update(result)
        return data
