from copy import deepcopy

import lxml.etree

from .webscraper import xpath_returns_text


def show_keys(keys):
    return ''.join(map('[{!r}]'.format, keys))


def verbose_scrape(etree, xpaths, keys=None, xpath=None, steps=None, sep='--'):
    data = {}
    if keys is None:
        keys, xpath, steps = [], [], []
    steps.append('Page content length: {}'.format(len(etree.text_content())))
    try:
        for key, value in xpaths.items():
            if isinstance(value, str):
                data[key] = etree.xpath(value)
                if xpath_returns_text(value):
                    data[key] = ''.join(data[key])
                steps.append('\n'.join((
                    '',
                    '  key:  ' + show_keys(keys + [key]),
                    '  xpath:' + '/'.join(xpath + [value]),
                    '  value:' + data[key]
                )))
            else:
                keys.append(key)
                xpath.append(value[0])
                data[key] = []
                nodes = etree.xpath(value[0])
                steps.append('\n'.join((
                    sep,
                    'key:     ' + show_keys(keys),
                    'xpath:   ' + '/'.join(xpath),
                    'elements: <{}> * {}'.format(nodes[0].tag, len(nodes)),
                    sep
                )))
                for n, node in enumerate(nodes):
                    fmt_xpath = ['({})[{}]'.format('/'.join(xpath), n + 1)]
                    s, d = verbose_scrape(node, value[1], keys=keys + [n],
                                          xpath=fmt_xpath, steps=steps,
                                          sep=sep)
                    data[key].append(d)
                    steps.append(sep[1:])
                xpath.pop()
    except (ValueError, lxml.etree.XPathSyntaxError,
            lxml.etree.XPathEvalError) as exception:
        steps.append(str(exception))
    return steps, deepcopy(data)
