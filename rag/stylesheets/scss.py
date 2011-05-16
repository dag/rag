from __future__ import absolute_import
from . import AbstractStylesheet
from ..utils import ReusableMixin
import scss


class Stylesheet(AbstractStylesheet, ReusableMixin):

    compress = False

    @property
    def compiler(self):
        if not hasattr(self, '_compiler'):
            self._compiler = scss.Scss()
            self._compiler.scss_opts.update(compress=self.compress)
        return self._compiler

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
