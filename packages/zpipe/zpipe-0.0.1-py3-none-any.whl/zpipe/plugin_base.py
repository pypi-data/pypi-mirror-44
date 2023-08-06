# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    plugin_base.py
   Author :       Zhang Fan
   date：         2019/4/11
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import re


class plugin_base():
    def __init__(self):
        self._extract_field_re = re.compile(r'^%\{(.*?)\}$')

    def plugin_init(self, **kw):
        '''
        插件初始化
        :param kw: 这里接收管道定义的插件参数
        '''
        pass

    def plugin_distroy(self):
        '''
        插件销毁时
        '''
        pass

    def process(self, data):
        '''
        插件过程
        :param data: 收到的数据
        :return: 结果会顺序传递给下一个插件, 如果是最后一个插件则会返回给管道的调用者
        '''
        return data

    def get_data_parent(self, raw_data, key):
        key_chain = key.split('.')
        out_key = key_chain.pop(-1)

        data_chain = raw_data
        for field in key_chain:
            data_chain = data_chain[field]
        return data_chain, out_key

    def extract_data(self, raw_data, key, default=None):
        if not key:
            return default

        search = self._extract_field_re.search(key)
        if not search:
            return key

        pop = False
        raw_field = search.group(1)

        if raw_field[0] == '^':
            pop = True
            raw_field = raw_field[1:]

        try:
            data_chain, field = self.get_data_parent(raw_data, raw_field)
            if pop:
                return data_chain.pop(field)
            return data_chain[field]
        except:
            raise Exception(f'在原始数据中无法取出{key}指向的数据')
