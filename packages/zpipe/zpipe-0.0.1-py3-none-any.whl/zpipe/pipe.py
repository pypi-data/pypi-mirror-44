# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    pipe.py
   Author :       Zhang Fan
   date：         2019/4/11
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import datetime
import importlib

from zpipe.codec import process as codec_process
from zpipe.codec import codec_destory

from zpipe import codec_exception
from zpipe import filter_exception
from zpipe import output_exception


class pipe:
    _plugin_type_list = ['codec', 'filter', 'output']
    _except_type_mapp = dict(
        codec=codec_exception,
        filter=filter_exception,
        output=output_exception
    )
    __attrs__ = dict(
        codec=None,
        filter=None,
        output=None,

        time_stamp=True,
    )

    def __init__(self, name, **kw):
        self.name = name
        self._config = {k: kw[k] if k in kw else v for k, v in self.__attrs__.items()}
        self._plugin_saver = self._load_plugin()

    def _load_plugin(self):
        result = []
        for plugin_type in self._plugin_type_list:
            plugin_name, plugin, codec = self._get_plugin_inst(plugin_type)
            if plugin_name:
                result.append((plugin_type, plugin_name, plugin, codec))
        return result

    def _get_plugin_inst(self, plugin_type):
        config = self._config.pop(plugin_type, None)
        if not config:
            return None, None, None

        if isinstance(config, str):
            config = dict(name=config)
        else:
            assert isinstance(config, dict), f'pipe<{self.name}>的配置错误'

        name = config.pop('name')
        codec_config = config.pop('codec', None)

        try:
            plugin_name = f'zpipe_{plugin_type}_{name}'
            module_file = importlib.import_module(plugin_name)
            cls = getattr(module_file, plugin_name)
            plugin = cls()
            plugin.plugin_init(**config)
        except:
            raise Exception(f'无法加载{plugin_type}插件<{name}>')

        if codec_config:
            if isinstance(codec_config, str):
                codec_config = dict(name=codec_config)
            else:
                assert isinstance(codec_config, dict), f'{plugin_type}插件<{name}>的解码器设置错误'

        return name, plugin, codec_config

    def _make_msg(self, data):
        result = dict(raw=data)
        if self._config.get('time_stamp'):
            result['@time_stamp'] = datetime.datetime.utcnow().isoformat()
        return result

    def process(self, data) -> object:
        data = self._make_msg(data)
        for plugin_type, plugin_name, plugin, codec_config in self._plugin_saver:
            data = codec_process(data, codec_config)
            try:
                data = plugin.process(data)
            except:
                exception = self._except_type_mapp[plugin_type]
                raise exception(f'{plugin_type}<{plugin_name}>过程错误')
        return data

    def distroy(self):
        for plugin_type, plugin_name, plugin, codec_config in self._plugin_saver:
            plugin.plugin_distroy()
        codec_destory()
