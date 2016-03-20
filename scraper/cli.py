import sys

import click
import json
import lxml
import requests

from .webscraper import scrape_page



@click.command()
@click.argument('-f', '--file', 'xpaths_filename', type=click.File(),
                help='name of JSON file containing xpaths')
@click.option('-P', '--page', 'html_filename', type=click.File('rb'),
              help='name of file containing HTML content')
@click.option('-x', '--xpath', 'xpath_expr'
              help='XPATH expression')
@click.option('-u', '--url',
              help='URL of web page to scrape')
def main(xpaths_filename, html_filename, xpath_expr, url):
    try:
        if xpath_expr:
            
         or (html_filename and not xpaths_filename):
        #    click.echo(lxml.etree.tostring(etree.xpath(cfg),
        #                                   pretty_print=True))
        result = scrape_page(json.load(xpaths_filename), page=html_filename)
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
