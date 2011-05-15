from abc import ABCMeta, abstractproperty


class AbstractDocument(object):
    __metaclass__ = ABCMeta

    def __init__(self, path):
        self.path = path

    @abstractproperty
    def meta(self):
        pass

    @abstractproperty
    def id(self):
        pass

    @abstractproperty
    def title(self):
        pass
