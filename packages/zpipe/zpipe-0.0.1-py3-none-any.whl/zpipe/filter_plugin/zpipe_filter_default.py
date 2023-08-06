# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    zpipe_filter_default.py
   Author :       Zhang Fan
   date：         2019/4/12
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

from zpipe import plugin_base


class zpipe_filter_default(plugin_base):
    __attrs__ = dict(
        remove=None
    )

    def plugin_init(self, **kw):
        self.config = {k: kw[k] if k in kw else v for k, v in self.__attrs__.items()}

        remove = self.config['remove']
        if isinstance(remove, str):
            remove = [remove]
        self.config['remove'] = remove or []

    def plugin_distroy(self):
        pass

    def process(self, raw_data):
        for key in self.config['remove']:
            try:
                data_chain, out_key = self.get_data_parent(raw_data, key)
                data_chain.pop(out_key)
            except:
                raise Exception(f'在原始数据中无法找到{key}指向的数据')

        return raw_data
