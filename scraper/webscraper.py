import json
import re

import lxml

XPATH_AS_STR_RE = re.compile(r'(text\(\)(\)\[\d+\])?|@[^/]+)$')


def xpath_returns_text(xpath_expr, xpath_as_str_re=XPATH_AS_STR_RE):
    return xpath_as_str_re.search(xpath_expr)


def compile_xpaths(xpaths):
    """
    :raises: lxml.etree.XPathSyntaxError
    :raises: lxml.etree.XPathEvalError
    """
    try:
        return {k: lxml.etree.XPath(v) if isinstance(v, str)
                else [lxml.etree.XPath(v[0]), compile_xpaths(v[1])]
                for k, v in xpaths.items()}
    except lxml.etree.XPathSyntaxError as e:
        raise lxml.etree.XPathSyntaxError(e.msg + '\n' + json.dumps(xpaths))
    except lxml.etree.XPathEvalError as e:
        raise lxml.etree.XPathEvalError(e.msg + '\n' + json.dumps(xpaths))


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


def scrape_page(config, etree):
    """Extract data from an Element Tree and put it into a JSON file

    The scraper uses recursive XPath expressions and keys defined in
    a JSON file to determine what to pull and where to put it.

    if page is set to None, the page is retrieved from the "_url' key
    if the config, else load the page from a file (or stdin)
    raises:

    Potential Exceptions:
        requests.RequestException, requests.HTTPError
        lxml.etree.XPathSyntaxError, lxml.etree.XPathEvalError
        lxml.etree.ParserError, UnicodeDecodeError
    """
    xpaths = {k: v for k, v in config.items() if not k.startswith('_')}
    return scrape(etree, compile_xpaths(xpaths))
