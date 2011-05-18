from . import AbstractSite
from brownie.caching import cached_property


class Site(AbstractSite):

    @cached_property
    def documents(self):
        return {}

    @cached_property
    def templates(self):
        return {}

    @cached_property
    def stylesheets(self):
        return {}

    @cached_property
    def histories(self):
        return []
