import json
import os
import sys
from functools import partial

import click
import jsonschema

from .exceptions import ScraperException
from .htmlpage import dump_etree_html, load_html_page, html2etree
from .loadjson import json_load
from .verbosescraper import verbose_scrape, text, color_label, color_separator
from .webscraper import do_xpath, scrape_page, xpath_returns_text

CONFIG_SCHEMA = 'scraperschema.json'


@click.command()
@click.option('-f', '--file', 'cfg_file', type=click.File(),
              help='name of JSON file containing xpaths')
@click.option('-i', '--indent', type=click.IntRange(min=0, max=8), default=2,
              help='indent size for output')
@click.option('-t', '--tidy', is_flag=True,
              help='tidy HTML (normalizes space & indent)')
@click.option('-u', '--url', help='URL of HTML page')
@click.option('-v', '--verbose', is_flag=True,
              help='display the results for each scraper step')
@click.option('-x', '--xpath', help='XPATH expression')
@click.option('-P', '--page', type=click.File('rb'),
              help='name of file containing HTML content')
@click.option('--raw', is_flag=True, help='bypass parser, output raw HTML')
@click.option('--keycolor', help='field colors (used by verbose)')
@click.option('--sepchar', default='-',
              help='separator character (used by verbose)')
@click.option('--sepsize', type=click.IntRange(min=0, max=300), default=76,
              help='number of characters in separator (used by verbose)')
@click.option('--sepcolor', default='yellow',
              help='separator color (used by verbose)')
def main(cfg_file, indent, tidy, url, verbose, xpath, page, raw,
         keycolor, sepchar, sepsize, sepcolor):
    config_schema = os.path.join(os.path.dirname(__file__), CONFIG_SCHEMA)
    try:
        config = json_load(cfg_file) if cfg_file else {}
        jsonschema.validate(config, json_load(open(config_schema)))
        html = load_html_page(config, page, url)
        if raw:
            return click.echo(html)

        etree = html2etree(html)
        sep = (color_separator(sepchar, sepsize, sepcolor)
               if sepcolor else sepchar * sepsize)

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
                label = (text if keycolor is None else
                         partial(color_label, color=keycolor))
                for line in verbose_scrape(etree, config, sep, label):
                    click.echo(line)
            else:
                result = scrape_page(etree, config)
                click.echo(json.dumps(result, indent, sort_keys=True))
        else:
            click.echo(dump_etree_html(etree, tidy, indent))

    except (EnvironmentError, UnicodeDecodeError, TypeError) as e:
        click.echo(str(e))
        sys.exit(1)
    except ScraperException as exception:
        exception.echo()
        sys.exit(1)

if __name__ == '__main__':
    main()
