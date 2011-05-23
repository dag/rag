import sys
from os import path
from abc import ABCMeta, abstractproperty


class OverridableMixin(object):

    @classmethod
    def but(cls, **overrides):
        return type(cls.__name__, (cls,), overrides)


class ModuleDirectory(object):
    __metaclass__ = ABCMeta

    def __init__(self, module, filename):
        self.module = module
        self.filename = filename

    @abstractproperty
    def __directory__(cls):
        pass

    @abstractproperty
    def extension(cls):
        pass

    @property
    def directory(self):
        return path_from_module(self.module, self.__directory__)

    @property
    def filepath(self):
        return path.join(self.directory, self.filename)

    @classmethod
    def configure(cls, site):
        site.register_type(cls.__directory__, cls.extension, cls)


def path_from_module(module, *paths):
    root = path.dirname(sys.modules[module].__file__)
    return path.abspath(path.join(root, *paths))
