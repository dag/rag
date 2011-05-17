from abc import ABCMeta, abstractproperty
from brownie.caching import cached_property


class AbstractHistory(object):
    __metaclass__ = ABCMeta

    def __init__(self, filepath):
        self.filepath = filepath

    @cached_property
    def created(self):
        return self.edits[0].timestamp

    @cached_property
    def author(self):
        return self.edits[0].author

    @cached_property
    def modified(self):
        return self.edits[-1].timestamp

    @abstractproperty
    def edits(self):
        pass


class AbstractEdit(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def timestamp(self):
        pass

    @abstractproperty
    def author(self):
        pass

    @abstractproperty
    def comment(self):
        pass
