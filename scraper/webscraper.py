import json
import re

import lxml

XPATH_AS_STR_RE = re.compile(r'(text\(\))|(/@[^/]+)$')


def xpath_returns_text(xpath_expr, xpath_as_str_re=XPATH_AS_STR_RE):
    """Does the XPath expression return text, as opposed to a Sequence?

    Returns:
      - True if the XPath ends with text() or @<attrib-name>
      - False if the XPath returns a Sequence of items
    """
    return bool(xpath_as_str_re.search(xpath_expr))


def get_xpath_val(value, xpath, xpath_returns_str=XPATH_AS_STR_RE):
    """Returns either the text value or a Sequence from XPath result"""
    return ''.join(value) if xpath_returns_text(xpath) else value


def compile_xpaths(xpaths):
    """Precompile the XPaths in the scraper config file

    Potential Exceptions:
      - lxml.etree.XPathSyntaxError
      - lxml.etree.XPathEvalError
    """
    try:
        return {k: lxml.etree.XPath(v) if isinstance(v, str)
                else [lxml.etree.XPath(v[0]), compile_xpaths(v[1])]
                for k, v in xpaths.items()}
    except lxml.etree.XPathSyntaxError as e:
        raise lxml.etree.XPathSyntaxError(e.msg + '\n' + json.dumps(xpaths))
    except lxml.etree.XPathEvalError as e:
        raise lxml.etree.XPathEvalError(e.msg + '\n' + json.dumps(xpaths))


def scrape(etree, xpaths):
    """Extract data from an Element Tree and put it into a JSON file

    The scraper uses recursive XPath expressions and keys defined in
    a JSON file to determine what to pull and where to put it.

    Potential Exceptions:
        - UnicodeDecodeError
        - lxml.etree.ParserError
    """
    return {k: get_xpath_val(v(etree), v.path)
            if isinstance(v, lxml.etree.XPath)
            else [scrape(i, v[1]) for i in v[0](etree)]
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
