from attest import assert_hook

from os import path
from rag import documents, histories
from attest import Tests

ROOT_PATH = path.abspath(path.dirname(__file__))
SAMPLE_DOC = path.join(ROOT_PATH, 'documents', 'sample.rst')


rst = Tests()

@rst.context
def rst_document():
    yield documents.Rst(SAMPLE_DOC)

@rst.test
def doc_properties(doc):
    assert doc.meta['type'] == 'blog'
    assert doc.id == 'this-is-a-sample-rest-document'
    assert doc.title == 'This is a Sample reST Document'


git = Tests()

@git.context
def git_history():
    yield histories.Git(SAMPLE_DOC)

@git.test
def history_properties(history):
    assert history.path_in_repo == 'tests/documents/sample.rst'

@git.test
def commits(history):
    assert len(history.commits) == 1
    assert history.commits[0].message == 'basic reST documents\n'
