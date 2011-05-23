from __future__ import absolute_import
from attest import assert_hook

import os
import time

from os import path
from textwrap import dedent
from datetime import date, datetime
from tempfile import NamedTemporaryFile
from attest import Tests, tempdir
from rag import utils, recipes, lazy

ROOT_PATH = path.abspath(path.dirname(__file__))
SAMPLE_DOC = path.join(ROOT_PATH, 'documents', 'sample.rst')


simple = Tests()

@simple.test
def path_from_module():
    assert utils.path_from_module(__name__) == ROOT_PATH
    assert utils.path_from_module(__name__, 'documents', 'sample.rst')\
        == SAMPLE_DOC


overrides = Tests()

@overrides.context
def class_with_overrides():

    class Archetype(utils.OverridableMixin):

        typical = 'default'

    yield Archetype, Archetype.but(typical='non-standard', more='less')

@overrides.test
def new_type_from_overrides(archetype, customized):
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
        extension = 'ext'

    yield Arbitrary(__name__, 'arbitrary-file.ext')

@directories.test
def arbitrary_file(arbitrary):
    assert arbitrary.module == __name__
    assert arbitrary.filename == 'arbitrary-file.ext'
    assert arbitrary.directory == path.join(ROOT_PATH, 'arbitraries')
    assert arbitrary.filepath\
        == path.join(ROOT_PATH, 'arbitraries', 'arbitrary-file.ext')


build = Tests(contexts=[tempdir])

@build.test
def index_dir(out):
    index = recipes.Directory()\
           .render('start.html', title='Hello!')\
           .with_context(subtitle='Hi you!')\
           .to_directory(out)
    assert index.path_as_file == index.path_as_directory == 'index.html'
    assert index.template == 'start.html'
    assert index.context == dict(title='Hello!', subtitle='Hi you!')
    assert index.filepath == path.join(out, 'index.html')
    assert not index.built

@build.test
def atom_file(out):
    atom = recipes.File('atom.xml').to_directory(out)
    assert atom.path_as_file == atom.path_as_directory == 'atom.xml'
    assert atom.filepath == path.join(out, 'atom.xml')
    assert not atom.built

@build.test
def sample_dir(out):
    doc = lazy.rst.Document(__name__, 'sample.rst')
    sample = recipes.Directory('posts', (2011, 5, 18), doc.id)\
            .render('post.html')\
            .for_document(doc)\
            .to_directory(out)
    assert sample.context['document'] == doc
    assert sample.path_as_file\
        == 'posts/2011/5/18/this-is-a-sample-rest-document.html'
    assert sample.path_as_directory\
        == 'posts/2011/5/18/this-is-a-sample-rest-document/index.html'
    assert sample.filepath == path.join(out, sample.path_as_directory)
    assert not sample.built
    os.makedirs(path.dirname(sample.filepath))
    with open(sample.filepath, 'w') as f:
        f.write('')
    doctime = int(path.getmtime(doc.filepath))
    os.utime(sample.filepath, (doctime, doctime))
    assert sample.built


rst = Tests()

@rst.context
def rst_document():
    yield lazy.rst.Document(__name__, 'sample.rst')

@rst.test
def rst_properties(doc):
    assert doc.meta['type'] == 'blog'
    assert doc.id == 'this-is-a-sample-rest-document'
    assert doc.title == 'This is a Sample reST Document'

@rst.test
def parts(doc):
    assert doc.parts['html_title']\
        == '<h1 class="title">This is a Sample reST Document</h1>\n'


git = Tests()

@git.context
def git_history():
    yield lazy.git.History(SAMPLE_DOC)

@git.test
def history_properties(history):
    assert history.path_in_repo == 'tests/documents/sample.rst'

@git.test
def commits(history):
    assert len(history.commits) == 1
    assert history.commits[0].message == 'basic reST documents\n'

@git.test
def edits(history):
    assert len(history.edits) == 1
    assert history.edits[0].comment == 'basic reST documents\n'
    assert str(history.edits[0].author) == 'Dag Odenhall'
    assert history.author == history.edits[0].author
    assert history.created.date() == date(2011, 5, 14)
    assert history.created == history.modified == history.edits[0].timestamp


fs = Tests()

@fs.context
def tempfile():
    with NamedTemporaryFile() as tf:
        os.utime(tf.name, (666, 666))
        yield lazy.fs.History(tf.name)

@fs.test
def file_timestamps(history):
    assert history.created == history.modified == datetime.fromtimestamp(666)

@fs.test
def file_author(history):
    try:
        import pwd
        pw = pwd.getpwuid(os.getuid())
        name = pw.pw_name
        fullname = pw.pw_gecos.split(',')[0]
    except ImportError:
        name = None
    assert history.edits[0].author in {name, fullname}
    assert history.author == history.edits[0].author


html = Tests()

@html.context
def genshi_html_template():
    yield lazy.genshi.Template(__name__, 'index.html')

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
    yield lazy.genshi.XmlTemplate(__name__, 'atom.xml')

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
    yield lazy.genshi.TextTemplate(__name__, 'robots.txt')

@text.test
def robots(template):
    assert template.render(rules={'*': '/'}) == dedent("""\
        User-Agent: *
        Disallow: /
        """)


scss = Tests()

@scss.context
def scss_stylesheet():
    yield lazy.scss.Stylesheet(__name__, 'main.scss')

@scss.test
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


bare = Tests()

@bare.context
def bare_site():
    site = lazy.bare.Site(__name__)
    site.use(lazy.rst, lazy.genshi, lazy.scss, lazy.git, lazy.fs)
    yield site

@bare.test
def rst_for_docs(site):
    assert site.documents == dict(rst=lazy.rst.Document)

@bare.test
def genshi_for_templates(site):
    assert site.templates == dict(html=lazy.genshi.Template,
                                  xml=lazy.genshi.XmlTemplate,
                                  txt=lazy.genshi.TextTemplate)

@bare.test
def scss_for_styles(site):
    assert site.stylesheets == dict(scss=lazy.scss.Stylesheet)

@bare.test
def git_and_fs_histories(site):
    assert site.histories == [lazy.git.History, lazy.fs.History]
