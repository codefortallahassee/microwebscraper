import sys

import click
import json
import lxml.etree
import lxml.html
import requests

from .htmlpage import load_html_page
from .webscraper import scrape_page, xpath_returns_text


def etree2html(etree):
    result = lxml.html.tostring(etree, pretty_print=True)
    return result.replace(b'&#13;', b'')


@click.command()
@click.option('-f', '--file', 'cfg_file', type=click.File(),
              help='name of JSON file containing xpaths')
@click.option('-x', '--xpath', help='XPATH epxression')
@click.option('-u', '--url', help='URL of HTML page')
@click.option('-P', '--page', type=click.File('rb'),
              help='name of file containing HTML content')
@click.option('-s', '--sep', default=b'-', type=bytes,
              help='output list separator')
def main(cfg_file, xpath, url, page, sep):
    try:
        config = json.load(cfg_file) if cfg_file else {}
        etree = lxml.html.fromstring(load_html_page(config, page, url))
        if config:
            result = scrape_page(config, etree)
            click.echo(json.dumps(result, indent=4, sort_keys=True))
            return

        if not xpath:
            click.echo(etree2html(etree))
            return

        results = etree.xpath(xpath)
        if not results:
            return

        if xpath_returns_text(xpath):
            click.echo('\n'.join(results))
            return

        separator = sep * 78 + b'\n'
        elements = map(etree2html, results)
        click.echo(separator + (separator).join(elements) + separator)

    except (
        EnvironmentError, json.JSONDecodeError,
        requests.RequestException, requests.HTTPError,
        lxml.etree.ParseError, UnicodeDecodeError,
        lxml.etree.XPathSyntaxError, lxml.etree.XPathEvalError
    ) as exception:
        click.echo(str(exception), err=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
