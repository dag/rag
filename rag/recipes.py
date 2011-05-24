from abc import ABCMeta, abstractproperty
from os import path
import errno
from brownie.itools import flatten
from brownie.caching import cached_property
from .utils import OverridableMixin


class AbstractRecipe(object):
    __metaclass__ = ABCMeta

    def __init__(self, *paths):
        self.paths = map(str, flatten(paths))
        self.path = '/'.join(self.paths)
        self.context = {}

    @abstractproperty
    def path_as_file(self):
        pass

    @abstractproperty
    def path_as_directory(self):
        pass

    def render(self, template, **context):
        self.template = template
        self.context.update(context)
        return self

    def with_context(self, **context):
        self.context.update(context)
        return self

    def for_document(self, document):
        self.document = document
        self.context.update(document=document)
        return self

    def to_directory(self, path, in_format='directory'):
        self.output_directory = path
        self.build_format = in_format
        return self

    @cached_property
    def filepath(self):
        return path.abspath(path.join(self.output_directory,
            getattr(self,
                {'file': 'path_as_file',
                 'directory': 'path_as_directory'}[self.build_format])))

    @property
    def built(self):
        try:
            return int(path.getmtime(self.document.filepath))\
                == int(path.getmtime(path.join(self.output_directory,
                                               self.filepath)))
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
        except AttributeError:
            pass
        return False


class Page(AbstractRecipe, OverridableMixin):

    extension = '.html'

    @cached_property
    def path_as_file(self):
        if self.path:
            return self.path + self.extension
        return 'index' + self.extension

    @cached_property
    def path_as_directory(self):
        if self.path:
            return self.path + '/index' + self.extension
        return 'index' + self.extension


class File(AbstractRecipe):

    @cached_property
    def path_as_file(self):
        return self.path

    @cached_property
    def path_as_directory(self):
        return self.path
