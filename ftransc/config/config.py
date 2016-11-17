import os
import copy
import json


class BaseConfig(object):
    config_file = ''

    def __init__(self):
        self.__data = {}
        self.__parse()

    def __parse(self):
        if self.config_file:
            config_file = os.path.join(os.path.dirname(__file__), 'data', self.config_file)
            with open(config_file) as fd:
                self.__data = json.load(fd)

    def __getattr__(self, item):
        try:
            return self.__data[item]
        except KeyError:
            raise AttributeError(item)

    def get(self, key, default=None):
        return self.__data.get(key, default)

    def as_dict(self):
        return copy.deepcopy(self.__data)


class AudioPresets(BaseConfig):
    config_file = 'presets.json'


class TagMap(BaseConfig):
    config_file = 'tagmap.json'
