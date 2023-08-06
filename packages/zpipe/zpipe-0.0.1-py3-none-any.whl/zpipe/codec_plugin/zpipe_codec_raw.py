# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    zpipe_codec_raw.py
   Author :       Zhang Fan
   date：         2019/4/12
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

from zpipe import plugin_base


class zpipe_codec_raw(plugin_base):
    def process(self, data):
        return data['raw']
