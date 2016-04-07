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


def text(label):
    return label


def color_label(label, color=LABEL_COLOR):
    return click.style(label, color)


def alert(label, color='red', bold=True):
    return click.style(label, fg=color, bold=bold)


def color_separator(sepchar=SEPARATOR_CHAR, sepsize=SEPARATOR_SIZE,
                    sepcolor=SEPARATOR_COLOR):
    return click.style(sepchar * sepsize, fg=sepcolor)


def first(seq):
    try:
        return seq[0]
    except IndexError:
        return repr(seq)


def get_tag(seq):
    el = first(seq)
    return el if isinstance(el, str) else '<{}>'.format(seq[0].tag)


def verbose_scrape(etree, config, sep='', label=text, keys=None, xpath=None):
    # import pdb; pdb.set_trace()

    if keys is None:
        keys, xpath = [], []
    yield label('Page content length: ') + str(len(etree.text_content()))
    for key, value in config.items():
        if isinstance(value, str) and xpath_returns_text(value):
            result = first(do_xpath(value, etree))
            if not result:
                result = alert(repr(result))
            yield ''
            yield label('  key:   ') + show_keys(keys + [key])
            yield label('  xpath: ') + '/'.join(xpath + [value])
            yield label('  value: ') + result
        else:
            keys.append(key)
            xpath.append(value[0])
            nodes = do_xpath(value[0], etree)
            tag = get_tag(nodes)
            yield sep
            yield label('key:      ') + show_keys(keys)
            yield label('xpath:    ') + '/'.join(xpath)
            yield label('elements: ') + '{} * {}'.format(tag, len(nodes))
            yield sep
            for n, node in enumerate(nodes):
                fmt_xpath = ['({})[{}]'.format('/'.join(xpath), n + 1)]
                for step in verbose_scrape(node, value[1], sep, label,
                                           keys + [n], fmt_xpath):
                    yield step
                yield sep
            xpath.pop()
