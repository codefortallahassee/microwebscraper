import json
import os

from nose.tools import assert_equals
from behave import given, when, then
from click.testing import CliRunner

import scraper.cli

runner = CliRunner()
current_dir = os.path.dirname(__file__)


@given('a config file named "{cfg_file}"')
def step_given_a_config_file(context, cfg_file):
    context.cfg_file = cfg_file


@given('a HTML file named "{page}"')
def step_and_a_html_file(context, page):
    context.page = page


@when('page is scraped')
def step_scrape_page(context):
    context.result = runner.invoke(scraper.cli.main, [
        '--file', os.path.join(current_dir, context.cfg_file),
        '--page', os.path.join(current_dir, context.page)]).output


@then('the data should match "{output}"')
def step_scrape(context, output):
    result = open(os.path.join(current_dir, output))
    assert_equals(json.loads(context.result), json.load(result))
