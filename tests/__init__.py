from __future__ import absolute_import
from attest import assert_hook

from os import path
from textwrap import dedent
from datetime import date
from rag import utils
from rag.documents import rst
from rag.histories import git
from rag.templates import genshi
from rag.stylesheets import scss
from attest import Tests

ROOT_PATH = path.abspath(path.dirname(__file__))
SAMPLE_DOC = path.join(ROOT_PATH, 'documents', 'sample.rst')


simple = Tests()

@simple.test
def path_from_module():
    assert utils.path_from_module(__name__) == ROOT_PATH
    assert utils.path_from_module(__name__, 'documents', 'sample.rst')\
        == SAMPLE_DOC


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


directories = Tests()

@directories.context
def module_directory():

    class Arbitrary(utils.ModuleDirectory):
        __directory__ = 'arbitraries'

    yield Arbitrary(__name__, 'arbitrary-file.ext')

@directories.test
def arbitrary_file(arbitrary):
    assert arbitrary.module == __name__
    assert arbitrary.filename == 'arbitrary-file.ext'
    assert arbitrary.directory == path.join(ROOT_PATH, 'arbitraries')
    assert arbitrary.filepath\
        == path.join(ROOT_PATH, 'arbitraries', 'arbitrary-file.ext')


documents = Tests()

@documents.context
def rst_document():
    yield rst.Document(__name__, 'sample.rst')

@documents.test
def doc_properties(doc):
    assert doc.meta['type'] == 'blog'
    assert doc.id == 'this-is-a-sample-rest-document'
    assert doc.title == 'This is a Sample reST Document'

@documents.test
def parts(doc):
    assert doc.parts['html_title']\
        == '<h1 class="title">This is a Sample reST Document</h1>\n'


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

@histories.test
def edits(history):
    assert len(history.edits) == 1
    assert history.edits[0].comment == 'basic reST documents\n'
    assert str(history.edits[0].author) == 'Dag Odenhall'
    assert history.created.date() == date(2011, 5, 14)
    assert history.created == history.modified == history.edits[0].timestamp


html = Tests()

@html.context
def genshi_html_template():
    yield genshi.Template(__name__, 'index.html')

@html.test
def index(template):
    assert template.render(generator='Rag') == dedent("""\
        <!DOCTYPE html>
        <html>
          <body>
            <h1>Welcome to this Rag site!</h1>
          </body>
        </html>""")


xml = Tests()

@xml.context
def genshi_xml_template():
    yield genshi.XmlTemplate(__name__, 'atom.xml')

@xml.test
def atom(template):
    assert template.render(generator='Rag') == dedent("""\
        <?xml version="1.0" encoding="utf-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
          <title>Recently posted on this Rag site</title>
        </feed>""")


text = Tests()

@text.context
def genshi_text_template():
    yield genshi.TextTemplate(__name__, 'robots.txt')

@text.test
def robots(template):
    assert template.render(rules={'*': '/'}) == dedent("""\
        User-Agent: *
        Disallow: /
        """)


stylesheets = Tests()

@stylesheets.context
def scss_stylesheet():
    yield scss.Stylesheet(__name__, 'main.scss')

@stylesheets.test
def main(stylesheet):
    assert stylesheet.render() == dedent("""\
        #navbar {
          border-bottom-color: #ce4dd6;
          border-bottom-style: solid;
        }
        .selector a {
          display: block;
        }
        .selector strong {
          color: #0000ff;
        }

        """)
