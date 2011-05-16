from __future__ import absolute_import
from ..utils import ReusableMixin, path_from_module
from . import AbstractTemplate
from genshi.template import TemplateLoader


_loaders = {}


class Template(AbstractTemplate, ReusableMixin):

    serializer = 'html'
    doctype = 'html5'

    @property
    def loader(self):
        if self.module not in _loaders:
            templates = path_from_module(self.module, 'templates')
            _loaders[self.module] = TemplateLoader([templates])
        return _loaders[self.module]

    def render(self, **context):
        template = self.loader.load(self.filename)
        stream = template.generate(**context)
        return stream.render(self.serializer, doctype=self.doctype)


class XmlTemplate(Template):

    serializer = 'xml'
    doctype = None
