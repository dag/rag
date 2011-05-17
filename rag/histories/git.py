from __future__ import absolute_import
from . import AbstractHistory, AbstractEdit
from git import Repo
from datetime import datetime


class History(AbstractHistory):

    @property
    def repo(self):
        return Repo(self.filepath)

    @property
    def path_in_repo(self):
        return self.filepath[len(self.repo.git_dir) - 4:]

    @property
    def commits(self):
        hashes = self.repo.git.log('--', self.path_in_repo, pretty='format:%H')
        return [self.repo.commit(h) for h in hashes.splitlines()]

    @property
    def edits(self):
        return map(Edit, self.commits)


class Edit(AbstractEdit):

    def __init__(self, commit):
        self.commit = commit

    @property
    def timestamp(self):
        return datetime.fromtimestamp(self.commit.authored_date)

    @property
    def author(self):
        return self.commit.author

    @property
    def comment(self):
        return self.commit.message
