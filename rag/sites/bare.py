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

    def recipes(self):
        documents = list(self)
        for builder in self.document_builders:
            for document in documents:
                for recipe in builder(document):
                    yield recipe.for_document(document)
        for builder in self.builders:
            for recipe in builder(documents):
                yield recipe

    @cached_property
    def document_builders(self):
        return []

    def build_document(self, builder):
        self.document_builders.append(builder)
        return builder

    @cached_property
    def builders(self):
        return []

    def build(self, builder):
        self.builders.append(builder)
        return builder
