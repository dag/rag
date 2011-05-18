from apipkg import initpkg

initpkg(__name__,
    dict(
        rst='rag.documents.rst',
        fs='rag.histories.fs',
        git='rag.histories.git',
        scss='rag.stylesheets.scss',
        genshi='rag.templates.genshi',
        bare='rag.sites.bare',
        Site='rag.sites.default:Site',
    )
)
