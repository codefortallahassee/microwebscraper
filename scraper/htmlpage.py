import requests
from copy import deepcopy

import lxml.html


def etree2html(etree):
    """renders an Element Tree (lxml.etree) as HTML (bytes)"""
    result = lxml.html.tostring(etree, pretty_print=True)
    return result.replace(b'&#13;', b'')


def html2etree(tag_soup):
    """parses HTML (bytes), returns an Element Tree (lxml.etree)

    exceptions:
        - UnicodeDecodeError
        - lxml.etree.ParserError
    """
    return lxml.html.fromstring(tag_soup)


def request_page(url, **kwargs):
    response = requests.get(url, **kwargs)
    response.raise_for_status()
    return response.content


def get_request_settings(config):
    """Pull requests.get settings from config dictionary"""
    cfg = deepcopy(config)
    url = cfg.pop('_url', None)
    return url, {k: v for k, v in cfg.items() if k.startswith('_')}


def load_html_page(config, page=None, url=None):
    if page:
        return page.read()

    requests_url, requests_kwargs = get_request_settings(config)
    return request_page(url if url else requests_url, **requests_kwargs)
