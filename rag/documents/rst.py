from brownie.caching import cached_property
from docutils import core, nodes
from . import AbstractDocument
from ..utils import ReusableMixin


class Document(AbstractDocument, ReusableMixin):
    __extension__ = 'rst'

    settings = None

    @cached_property
    def parts(self):
        with open(self.filepath) as f:
            return core.publish_parts(f.read(),
                source_path=self.filepath,
                writer_name='html',
                settings_overrides=self.settings)

    @cached_property
    def doctree(self):
        with open(self.filepath) as f:
            src = f.read()
        return core.publish_doctree(src,
            source_path=self.filepath,
            settings_overrides=self.settings)

    @cached_property
    def meta(self):
        return {name.astext().lower(): body.astext()
                for name, body in self.doctree.traverse(nodes.field)}

    @cached_property
    def id(self):
        return self.doctree.attributes['ids'][0]

    @cached_property
    def title(self):
        return self.doctree.attributes['title']


configure = Document.configure
