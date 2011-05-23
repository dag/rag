from __future__ import absolute_import
from ..utils import OverridableMixin
from . import AbstractTemplate
from genshi.template import TemplateLoader, NewTextTemplate


_loaders = {}


class Template(AbstractTemplate, OverridableMixin):

    class_ = None
    serializer = 'html'
    doctype = 'html5'

    @property
    def loader(self):
        if self.module not in _loaders:
            _loaders[self.module] = TemplateLoader([self.directory])
        return _loaders[self.module]

    def render(self, **context):
        template = self.loader.load(self.filename, cls=self.class_)
        stream = template.generate(**context)
        if self.doctype is None:
            return stream.render(self.serializer)
        return stream.render(self.serializer, doctype=self.doctype)


class XmlTemplate(Template):
    extension = 'xml'

    serializer = 'xml'
    doctype = None


class TextTemplate(Template):
    extension = 'txt'

    class_ = NewTextTemplate
    serializer = 'text'
    doctype = None


def configure(site):
    site.use(Template, XmlTemplate, TextTemplate)
