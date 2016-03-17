import lxml.html


def html2etree(tag_soup):
    """A HTML parser that returns an Element Tree.

    :rtype: lxml.etree
    :raises: UnicodeDecodeError
    :raises: lxml.etree.ParserError
    """
    return lxml.html.fromstring(tag_soup)
