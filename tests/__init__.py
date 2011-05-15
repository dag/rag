from __future__ import absolute_import
from attest import assert_hook

from os import path
from rag import utils
from rag.documents import rst
from rag.histories import git
from rag.templates import genshi
from attest import Tests

ROOT_PATH = path.abspath(path.dirname(__file__))
SAMPLE_DOC = path.join(ROOT_PATH, 'documents', 'sample.rst')


reusable = Tests()

@reusable.context
def reusable_class():

    class Archetype(utils.ReusableMixin):

        typical = 'default'

    yield Archetype, Archetype.using(typical='non-standard', more='less')

@reusable.test
def reusable_types(archetype, customized):
    assert archetype.typical == 'default'
    assert not hasattr(archetype, 'more')
    assert customized.typical == 'non-standard'
    assert customized.more == 'less'
    assert issubclass(customized, archetype)
    assert customized.__name__ == archetype.__name__


documents = Tests()

@documents.context
def rst_document():
    yield rst.Document(SAMPLE_DOC)

@documents.test
def doc_properties(doc):
    assert doc.meta['type'] == 'blog'
    assert doc.id == 'this-is-a-sample-rest-document'
    assert doc.title == 'This is a Sample reST Document'


histories = Tests()

@histories.context
def git_history():
    yield git.History(SAMPLE_DOC)

@histories.test
def history_properties(history):
    assert history.path_in_repo == 'tests/documents/sample.rst'

@histories.test
def commits(history):
    assert len(history.commits) == 1
    assert history.commits[0].message == 'basic reST documents\n'


templates = Tests()

@templates.context
def genshi_html_template():
    yield genshi.Template

@templates.context
def genshi_xml_template():
    yield genshi.Template.using(serializer='xml', doctype=None)

@templates.test
def serializer(html, xml):
    assert html.serializer == 'html'
    assert xml.serializer == 'xml'

@templates.test
def doctype(html, xml):
    assert html.doctype == 'html5'
    assert xml.doctype == None
