from operator import attrgetter
from rag import Site, Directory, File

site = Site(__name__)

# document builders are called for each document
# and yield build recipes that are associated with the source document
# letting us compare sources and builds by mtime etc
@site.build_document
def docbuilder(document):
    if document.type == 'blog':

        # build /2011/05/hello-world/index.html
        # or    /2011/05/hello-world.html
        # depending on configuration
        yield Directory(document.created.year,
                        format(document.created.month, '02'),
                        document.name).render('post.html')

# normal builders are not bound to any particular document
# and instead assumed to always need rebuilding
@site.build
def builder(documents):
    new = sorted(documents, key=attrgetter('modified'))[:5]

    # build /recent.xml
    yield File('recent.xml').render('atom.xml', documents=new)

    # build /index.html
    yield Directory().render('posts.html', documents=new)

    years = {doc.created.year for doc in documents}
    for year in years:
        docs = [doc for doc in documents if document.created.year == year]

        # build /2011/index.html or /2011.html
        yield Directory(year).render('summaries.html', documents=docs)

        months = {doc.created.month for doc in docs}
        for month in months:
            docs = [doc for doc in docs if document.created.month == month]

            # build /2011/05/index.html or /2011/05.html
            yield Directory(year, format(month, '02'))\
                    .render('posts.html', documents=docs)
