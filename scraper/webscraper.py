import re

import lxml

import htmlparser
import pagerequest
import requestsfile

XPATH_AS_STR_RE = re.compile(r'(text\(\)(\)\[\d+\])?|@[^/]+)$')


def compile_xpaths(xpaths):
    """
    :raises: lxml.etree.XPathSyntaxError
    :raises: lxml.etree.XPathEvalError
    """
    return {k: lxml.etree.XPath(v) if isinstance(v, str)
            else [lxml.etree.XPath(v[0]), compile_xpaths(v[1])]
            for k, v in xpaths.items()}


def get_xpath_val(value, xpath, xpath_returns_str=XPATH_AS_STR_RE):
    return ''.join(value) if xpath_returns_str.search(xpath) else value


def scrape(etree, xpaths):
    """
    :raises: UnicodeDecodeError
    :raises: lxml.etree.ParserError
    """
    return {k: get_xpath_val(v(etree), v.path)
            if isinstance(v, lxml.etree.XPath)
            else [scrape(i, v[1]) for i in v[0](etree)]
            for k, v in xpaths.items()}


def scrape_page(config):
    """Extract data from an Element Tree and put it into a JSON file

    The scraper uses recursive XPath expressions and keys defined in
    a JSON file to determine what to pull and where to put it.

    :returns: dict (JSON compatible)
    :raises: requests.RequestException
    :raises: requests.HTTPError
    :raises: lxml.etree.XPathSyntaxError
    :raises: lxml.etree.XPathEvalError
    :raises: lxml.etree.ParserError
    :raises: UnicodeDecodeError
    """
    url, kwargs = requestsfile.extract_request_args(config)
    page_content = pagerequest.get_page(url, **kwargs)
    etree = htmlparser.html2etree(page_content)

    xpaths = {k: v for k, v in config.items() if not k.startswith('_')}
    return scrape(etree, compile_xpaths(xpaths))
