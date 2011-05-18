from abc import ABCMeta, abstractproperty


class AbstractSite(object):
    __metaclass__ = ABCMeta

    def __init__(self, module):
        self.module = module

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
