import sys

import click
import json
import lxml
import requests

import webscraper

# if xpath:
#    click.echo(lxml.etree.tostring(etree.xpath(cfg),
#                                   pretty_print=True))


@click.command()
@click.argument('xpaths_file', type=click.File())
def main(xpaths_file):
    try:
        result = webscraper.scrape_page(json.load(xpaths_file))
        click.echo(json.dumps(result, indent=4, sort_keys=True))
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
