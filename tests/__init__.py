from os import path
from rag import documents
from attest import Tests

ROOT_PATH = path.abspath(path.dirname(__file__))

rst = Tests()

@rst.context
def rst_document():
    yield documents.Rst(path.join(ROOT_PATH, 'documents', 'sample.rst'))

@rst.test
def properties(doc):
    assert doc.meta['type'] == 'blog'
    assert doc.id == 'this-is-a-sample-rest-document'
    assert doc.title == 'This is a Sample reST Document'
