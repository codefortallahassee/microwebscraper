import os.path

from behave import when
from click.testing import CliRunner

import scraper.cli

runner = CliRunner()
current_dir = os.path.dirname(__file__)


@when('the file can not be found')
def step_file_not_found(context):
    context.output = runner.invoke(scraper.cli.main, [
        '--page', os.path.join(current_dir, context.page)]).output


@when('the page is scraped')
def step_scrape_page(context):
    context.output = runner.invoke(scraper.cli.main, [
        '--file', os.path.join(current_dir, context.cfg_file),
        '--page', os.path.join(current_dir, context.page)]).output


@when('the tidy option is selected')
def step_tidy_html(context):
    context.output = runner.invoke(scraper.cli.main, [
        '--page', os.path.join(current_dir, context.page),
        '--tidy']).output


@when('the XPath expression is processed against the HTML')
def step_do_xpath(context):
    context.output = runner.invoke(scraper.cli.main, [
        '--page', os.path.join(current_dir, context.page),
        '--xpath', context.xpath
    ]).output
