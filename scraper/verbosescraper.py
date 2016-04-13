import click

from webscraper import do_xpath, xpath_returns_text


def color_alert(label, color='red', bold=True):
    return click.style(repr(label), fg=color, bold=bold)


def color_label(label, color='green'):
    return click.style(label, color)


def color_separator(sepchar='-', sepsize=76, sepcolor='yellow'):
    return click.style(sepchar * sepsize, fg=sepcolor)


def show_keys(keys):
    return ''.join(map('[{!r}]'.format, keys))


def get_first_element(nodes):
    try:
        return nodes[0]
    except IndexError:
        return repr(nodes)


def get_tag(elements):
    first = get_first_element(elements)
    return first if isinstance(first, str) else '<{}>'.format(elements[0].tag)


def verbose_scrape(etree, config, sep=color_separator, label=color_label,
                   alert=color_alert, keys=None, xpath=None):
    if keys is None:
        keys, xpath = [], []
    yield label('Page content length: ') + str(len(etree.text_content()))
    for key, value in config.items():
        if isinstance(value, str) and xpath_returns_text(value):
            result = get_first_element(do_xpath(value, etree))
            yield ''
            yield label('  key:   ') + show_keys(keys + [key])
            yield label('  xpath: ') + '/'.join(xpath + [value])
            yield label('  value: ') + result if result else alert(result)
        else:
            keys.append(key)
            xpath.append(value[0])
            elements = do_xpath(value[0], etree)
            tag = get_tag(elements)
            yield sep
            yield label('key:      ') + show_keys(keys)
            yield label('xpath:    ') + '/'.join(xpath)
            yield label('elements: ') + '{} * {}'.format(tag, len(elements))
            yield sep
            for n, node in enumerate(elements):
                fmt_xpath = ['({})[{}]'.format('/'.join(xpath), n + 1)]
                for step in verbose_scrape(node, value[1], sep, label, alert,
                                           keys + [n], fmt_xpath):
                    yield step
                yield sep
            xpath.pop()
