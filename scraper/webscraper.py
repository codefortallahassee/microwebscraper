import re
import sys

import lxml
import lxml.etree

from .exceptions import InvalidXPathExpression

XPATH_AS_STR_RE = re.compile(r'(text\(\))|(/@[^/]+)$')


def xpath_returns_text(xpath_expr, xpath_as_str_re=XPATH_AS_STR_RE):
    """Does the XPath expression return text, as opposed to a Sequence?

    Returns:
      - True if the XPath ends with text() or @<attrib-name>
      - False if the XPath returns a Sequence of items
    """
    return bool(xpath_as_str_re.search(xpath_expr))


def do_xpath(xpath, etree):
    try:
        return etree.xpath(xpath)
    except (lxml.etree.XPathSyntaxError, lxml.etree.XPathEvalError):
        raise InvalidXPathExpression(sys.exc_info[:2], value=xpath)


def get_xpath_val(value, xpath, xpath_returns_str=XPATH_AS_STR_RE):
    """Returns either the text value or a Sequence from XPath result"""
    return ''.join(value) if xpath_returns_text(xpath) else value


def compile_xpath(path_expr, key=None):
    try:
        return lxml.etree.XPath(path_expr)
    except lxml.etree.XPathSyntaxError:
        raise InvalidXPathExpression(sys.exc_info[:2], value=path_expr,
                                     key=key)


def compile_xpaths(xpaths):
    """Precompile the XPaths in the scraper config file

    Potential Exceptions:
      - lxml.etree.XPathSyntaxError
    """
    return {k: compile_xpath(v, k) if isinstance(v, str)
            else [compile_xpath(v[0], k), compile_xpaths(v[1])]
            for k, v in xpaths.items()}


def eval_xpath(xpath, etree, key=None):
    try:
        return xpath(etree)
    except lxml.etree.XPathEvalError as exception:
        etree_class = '<{}>'.format(etree.__class__.__name_)
        args = (('key', key), ('xpath', xpath.path), ('etree', etree_class))
        exception.args += args
        raise


def scrape(etree, xpaths):
    """Extract data from an Element Tree and put it into a JSON file

    The scraper uses recursive XPath expressions and keys defined in
    a JSON file to determine what to pull and where to put it.

    Potential Exceptions:
        - UnicodeDecodeError
        - lxml.etree.ParserError
    """
    return {k: get_xpath_val(eval_xpath(v, etree, k), v.path)
            if isinstance(v, lxml.etree.XPath)
            else [scrape(i, v[1]) for i in eval_xpath(v[0], etree, k)]
            for k, v in xpaths.items()}


def scrape_page(etree, config, verbose=False, sep=''):
    """Compile XPaths & scrape data from the Element Tree (lxml.etree)

    If page is set to None, the page is retrieved from the "_url' key
    otherwise load the page from a file or stdin.

    Potential Exceptions:
      - requests.RequestException, requests.HTTPError
      - lxml.etree.XPathSyntaxError, lxml.etree.XPathEvalError
      - lxml.etree.ParserError, UnicodeDecodeError
    """
    xpaths = {k: v for k, v in config.items() if not k.startswith('_')}
    return scrape(etree, compile_xpaths(xpaths))
