from __future__ import absolute_import
from brownie.caching import cached_property
from . import AbstractStylesheet
from ..utils import OverridableMixin
import scss


class Stylesheet(AbstractStylesheet, OverridableMixin):

    extension = 'scss'
    compress = False

    @cached_property
    def compiler(self):
        compiler = scss.Scss()
        compiler.scss_opts.update(compress=self.compress)
        return compiler

    def render(self):
        with open(self.filepath) as f:
            contents = f.read()
        _old = scss.LOAD_PATHS
        scss.LOAD_PATHS = ','.join([self.directory, scss.LOAD_PATHS])
        try:
            compiled = self.compiler.compile(contents)
        finally:
            scss.LOAD_PATHS = _old
        return compiled


configure = Stylesheet.configure
