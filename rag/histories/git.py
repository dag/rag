from __future__ import absolute_import
from brownie.caching import cached_property
from . import AbstractHistory, AbstractEdit
from git import Repo
from datetime import datetime


class Edit(AbstractEdit):

    def __init__(self, commit):
        self.commit = commit

    @cached_property
    def timestamp(self):
        return datetime.fromtimestamp(self.commit.authored_date)

    @cached_property
    def author(self):
        return self.commit.author

    @cached_property
    def comment(self):
        return self.commit.message


class History(AbstractHistory):

    @cached_property
    def repo(self):
        return Repo(self.filepath)

    @cached_property
    def path_in_repo(self):
        return self.filepath[len(self.repo.git_dir) - 4:]

    @cached_property
    def commits(self):
        hashes = self.repo.git.log('--', self.path_in_repo, pretty='format:%H')
        return [self.repo.commit(h) for h in hashes.splitlines()]

    @cached_property
    def edits(self):
        return map(Edit, self.commits)


configure = History.configure
