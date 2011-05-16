from abc import ABCMeta, abstractproperty
from ..utils import ModuleDirectory


class AbstractDocument(ModuleDirectory):
    __metaclass__ = ABCMeta
    __directory__ = 'documents'

    @abstractproperty
    def meta(self):
        pass

    @abstractproperty
    def id(self):
        pass

    @abstractproperty
    def title(self):
        pass
