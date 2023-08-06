# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    zpipe_codec_dict.py
   Author :       Zhang Fan
   date：         2019/4/12
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

from zpipe import plugin_base


class zpipe_codec_dict(plugin_base):
    def process(self, data):
        data.update(data.pop('raw'))
        return data
