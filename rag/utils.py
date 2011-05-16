import sys
from os import path


class ReusableMixin(object):

    @classmethod
    def using(cls, **overrides):
        return type(cls.__name__, (cls,), overrides)


class ModuleDirectory(object):

    def __init__(self, module, filename):
        self.module = module
        self.filename = filename

    @property
    def directory(self):
        return path_from_module(self.module, self.__directory__)

    @property
    def filepath(self):
        return path.join(self.directory, self.filename)


def path_from_module(module, *paths):
    root = path.dirname(sys.modules[module].__file__)
    return path.abspath(path.join(root, *paths))
