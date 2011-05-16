from abc import ABCMeta, abstractmethod


class AbstractTemplate(object):
    __metaclass__ = ABCMeta

    def __init__(self, module, filename):
        self.module = module
        self.filename = filename

    @abstractmethod
    def render(self, **context):
        pass
