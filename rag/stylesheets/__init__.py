from abc import ABCMeta, abstractmethod
from ..utils import ModuleDirectory


class AbstractStylesheet(ModuleDirectory):
    __directory__ = 'stylesheets'

    @abstractmethod
    def render(self):
        pass
