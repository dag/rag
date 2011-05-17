from docutils import core, nodes
from . import AbstractDocument
from ..utils import ReusableMixin


class Document(AbstractDocument, ReusableMixin):

    settings = None

    @property
    def parts(self):
        if not hasattr(self, '_parts'):
            with open(self.filepath) as f:
                self._parts = core.publish_parts(f.read(),
                    source_path=self.filepath,
                    writer_name='html',
                    settings_overrides=self.settings)
        return self._parts

    @property
    def doctree(self):
        if not hasattr(self, '_doctree'):
            with open(self.filepath) as f:
                src = f.read()
            self._doctree = core.publish_doctree(src,
                source_path=self.filepath,
                settings_overrides=self.settings)
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
        return self.doctree.attributes['title']
