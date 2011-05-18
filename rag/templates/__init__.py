from abc import ABCMeta, abstractmethod
from ..utils import ModuleDirectory


class AbstractTemplate(ModuleDirectory):
    __metaclass__ = ABCMeta
    __directory__ = 'templates'
    __extension__ = 'html'

    @abstractmethod
    def render(self, **context):
        pass
