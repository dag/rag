import sys
from os import path


class ReusableMixin(object):

    @classmethod
    def using(cls, **overrides):
        return type(cls.__name__, (cls,), overrides)


def path_from_module(module, *paths):
    root = path.dirname(sys.modules[module].__file__)
    return path.abspath(path.join(root, *paths))
