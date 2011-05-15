from git import Repo


class Git(object):

    def __init__(self, path):
        self.path = path
        self.repo = Repo(path)

    @property
    def path_in_repo(self):
        return self.path[len(self.repo.git_dir) - 4:]

    @property
    def commits(self):
        hashes = self.repo.git.log('--', self.path_in_repo, pretty='format:%H')
        return [self.repo.commit(h) for h in hashes.splitlines()]
