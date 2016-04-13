import os
import sys

import click

from .exceptions import ScraperException
from .htmlpage import dump_etree_html, load_html_page, html2etree
from .loadjson import json_load, validate_json, dump_json
from .verbosescraper import verbose_scrape, color_label, color_separator
from .webscraper import do_xpath, scrape_page, xpath_returns_text

CONFIG_SCHEMA = 'scraperschema.json'


@click.command()
@click.option('-c', '--config', type=click.File(),
              help='name of JSON config file containing request & xpath info')
@click.option('-i', '--indent', type=click.IntRange(min=0, max=8), default=2,
              help='indent size for output')
@click.option('-t', '--tidy', is_flag=True,
              help='tidy HTML (normalizes space & indent)')
@click.option('-u', '--url', help='URL of HTML page')
@click.option('-v', '--verbose', is_flag=True,
              help='display the results for each scraper step')
@click.option('-x', '--xpath', help='XPATH expression')
@click.option('-p', '--page', type=click.File('rb'),
              help='name of file containing HTML content')
@click.option('--raw', is_flag=True, help='bypass parser, output raw HTML')
def main(config, indent, tidy, url, verbose, xpath, page, raw):
    config_schema = os.path.join(os.path.dirname(__file__), CONFIG_SCHEMA)
    try:
        if config:
            cfg = json_load(config)
            validate_json(cfg, json_load(open(config_schema)))
        else:
            cfg = {}
        html = load_html_page(cfg, page, url)
        if raw:
            return click.echo(html)

        etree = html2etree(html)
        sep = color_separator()

        if xpath:
            results = do_xpath(xpath, etree)
            if results:
                if xpath_returns_text(xpath):
                    click.echo('\n'.join(results))
                else:
                    for i in results:
                        click.echo(dump_etree_html(i, tidy, indent))
                        click.echo(sep)

        elif config:
            if verbose:
                for line in verbose_scrape(etree, cfg, sep, color_label):
                    click.echo(line)
            else:
                result = scrape_page(etree, cfg)
                click.echo(dump_json(result, indent, tidy, sort_keys=True))
        else:
            click.echo(dump_etree_html(etree, tidy, indent))

    except (EnvironmentError, UnicodeDecodeError) as e:
        click.echo(str(e))
        sys.exit(1)
    except ScraperException as exception:
        exception.echo()
        sys.exit(1)

if __name__ == '__main__':
    main()
