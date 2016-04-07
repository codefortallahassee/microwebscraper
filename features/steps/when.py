import os.path

from behave import when
from click.testing import CliRunner

import scraper.cli
import scraper.webscraper

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


@when('the page is scraped with the verbose option')
def step_verbose_scrape_page(context):
    context.output = runner.invoke(scraper.cli.main, [
        '--file', os.path.join(current_dir, context.cfg_file),
        '--page', os.path.join(current_dir, context.page),
        '--verbose']).output


@when('When the page is scraped with verbose option and keys colored yellow')
def step_verbose_scrape_page_with_yellow_keys(context):
    context.output = runner.invoke(scraper.cli.main, [
        '--file', os.path.join(current_dir, context.cfg_file),
        '--page', os.path.join(current_dir, context.page),
        '--keycolor', 'yellow',
        '--verbose']).output


@when('the page is parsed')
def step_parsed_html(context):
    context.output = runner.invoke(scraper.cli.main, [
        '--page', os.path.join(current_dir, context.page)]).output


@when('the raw option is selected')
def step_raw_html(context):
    context.output = runner.invoke(scraper.cli.main, [
        '--page', os.path.join(current_dir, context.page),
        '--raw']).output


@when('the tidy option is selected')
def step_tidy_html(context):
    context.output = runner.invoke(scraper.cli.main, [
        '--page', os.path.join(current_dir, context.page),
        '--tidy']).output


@when('the XPath expression is compiled')
def step_compile_xpath(context):
    context.output = scraper.webscraper.compile_xpath(context.xpath)


@when('the XPath expression is processed against the HTML')
def step_do_xpath(context):
    context.output = runner.invoke(scraper.cli.main, [
        '--page', os.path.join(current_dir, context.page),
        '--xpath', context.xpath
    ]).output
    for i in context.output.splitlines():
        print(len(i))
