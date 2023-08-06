# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    codec.py
   Author :       Zhang Fan
   date：         2019/4/12
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import importlib

from zpipe import codec_exception

codec_plugin_mapp = dict()
codec_func_mapp = dict()


def load_codec_plugin(name, config):
    codec_func = codec_func_mapp.get(name)
    if codec_func:
        return codec_func

    try:
        plugin_name = f'zpipe_codec_{name}'
        module_file = importlib.import_module(plugin_name)
        cls = getattr(module_file, plugin_name)
        plugin = cls()
        plugin.plugin_init(**config)
    except:
        raise Exception(f'无法加载codec插件<{name}>, ')

    codec_func = getattr(plugin, 'process')
    codec_plugin_mapp[name] = plugin
    codec_func_mapp[name] = codec_func
    return codec_func


def process(data, codec_config):
    if not codec_config:
        return data

    codec_name = codec_config.pop('name')
    codec_func = load_codec_plugin(codec_name, codec_config)

    try:
        result = codec_func(data, **codec_config)
    except:
        raise codec_exception(f'codec<{codec_name}>无法解析数据')
    return result


def codec_destory():
    for name, plugin in codec_plugin_mapp.items():
        plugin.plugin_distroy()
