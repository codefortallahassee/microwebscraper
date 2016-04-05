from copy import deepcopy

import click

from .webscraper import do_xpath, xpath_returns_text

LABEL_COLOR = 'green'
SEPARATOR_CHAR = '-'
SEPARATOR_SIZE = 76
SEPARATOR_COLOR = 'yellow'
DEFAULT_SEPARATOR = click.style(SEPARATOR_CHAR * SEPARATOR_SIZE,
                                fg=SEPARATOR_COLOR)


def show_keys(keys):
    return ''.join(map('[{!r}]'.format, keys))


def plain_label(label):
    return label


def color_label(label, color=LABEL_COLOR):
    return click.style(label, color)


def color_separator(sepchar=SEPARATOR_CHAR, sepsize=SEPARATOR_SIZE,
                    sepcolor=SEPARATOR_COLOR):
    return click.style(sepchar * sepsize, fg=sepcolor)


def verbose_scrape(etree, xpaths, keys=None, xpath=None, steps=None,
                   sep='', label=plain_label):
    data = {}
    if keys is None:
        keys, xpath, steps = [], [], []
    steps.append('Page content length: {}'.format(len(etree.text_content())))
    for key, value in xpaths.items():
        if isinstance(value, str):
            data[key] = etree.xpath(value)
            if xpath_returns_text(value):
                data[key] = ''.join(data[key])
            steps.append('\n'.join((
                '',
                label('  key:  ') + show_keys(keys + [key]),
                label('  xpath:') + '/'.join(xpath + [value]),
                label('  value:') + data[key]
            )))
        else:
            keys.append(key)
            xpath.append(value[0])
            data[key] = []
            nodes = do_xpath(value[0], etree)
            steps.append('\n'.join((
                sep,
                label('key:      ') + show_keys(keys),
                label('xpath:    ') + '/'.join(xpath),
                label('elements: ') + '<{}> * {}'.format(nodes[0].tag,
                                                         len(nodes)),
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
    return steps, deepcopy(data)
