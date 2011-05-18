from __future__ import absolute_import
import os
from brownie.caching import cached_property
from . import AbstractHistory, AbstractEdit
from datetime import datetime


class Edit(AbstractEdit):

    comment = None

    def __init__(self, filepath):
        self.filepath = filepath

    @cached_property
    def stat(self):
        return os.stat(self.filepath)

    @cached_property
    def timestamp(self):
        return datetime.fromtimestamp(self.stat.st_mtime)

    @cached_property
    def author(self):
        try:
            from pwd import getpwuid
            pw = getpwuid(self.stat.st_uid)
            try:
                name = pw.pw_gecos.split(',')[0]
                if name:
                    return name
            except KeyError:
                pass
            return pw.pw_name
        except ImportError:
            pass


class History(AbstractHistory):

    @cached_property
    def edits(self):
        return [Edit(self.filepath)]


configure = History.configure
