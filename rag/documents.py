from abc import ABCMeta, abstractproperty
import docutils.core as rst
from docutils import nodes


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


class Rst(AbstractDocument):

    @property
    def parts(self):
        if not hasattr(self, '_parts'):
            with open(self.path) as f:
                self._parts = rst.publish_parts(f.read(),
                    source_path=self.path,
                    writer_name='html')
        return self._parts

    @property
    def doctree(self):
        if not hasattr(self, '_doctree'):
            with open(self.path) as f:
                src = f.read()
            self._doctree = rst.publish_doctree(src, source_path=self.path)
        return self._doctree

    @property
    def meta(self):
        if not hasattr(self, '_meta'):
            self._meta = {}
            for name, body in self.doctree.traverse(nodes.field):
                self._meta[name.astext().lower()] = body.astext()
        return self._meta

    @property
    def id(self):
        return self.doctree.attributes['ids'][0]

    @property
    def title(self):
        return self.parts['title']
