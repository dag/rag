import os
from abc import ABCMeta, abstractproperty, abstractmethod
from brownie.caching import cached_property
from ..utils import path_from_module


class AbstractSite(object):
    __metaclass__ = ABCMeta

    def __init__(self, module):
        self.module = module

    @cached_property
    def root_path(self):
        return path_from_module(self.module)

    @abstractproperty
    def documents(self):
        pass

    @abstractproperty
    def templates(self):
        pass

    @abstractproperty
    def stylesheets(self):
        pass

    @abstractproperty
    def histories(self):
        pass

    @abstractmethod
    def recipes(self):
        pass

    def register_type(self, directory, extension, factory):
        if directory not in {'documents', 'templates', 'stylesheets'}:
            raise ValueError('unknown site directory {!r}'.format(directory))
        mapping = getattr(self, directory)
        if extension in mapping:
            raise KeyError('extension {!r} already registered for directory {!r]}'
                           .format(extension, directory))
        mapping[extension] = factory

    def use(self, *types):
        for t in types:
            t.configure(self)

    def __iter__(self):
        for doc in os.listdir(path_from_module(self.module, 'documents')):
            ext = doc.split('.', 1)[1]
            try:
                yield self.documents[ext](self.module, doc)
            except KeyError:
                pass
