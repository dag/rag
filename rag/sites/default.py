from . import AbstractSite
from ..lazy import rst, genshi, scss, git, fs
from brownie.datastructures import ImmutableDict


class Site(AbstractSite):

    documents = ImmutableDict(rst=rst.Document)
    templates = ImmutableDict(html=genshi.Template,
                              xml=genshi.XmlTemplate,
                              txt=genshi.TextTemplate)
    stylesheets = ImmutableDict(scss=scss.Stylesheet)
    histories = (git.History, fs.History)
