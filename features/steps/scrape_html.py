import json
import os

from behave import given, then
from click.testing import CliRunner

import scraper.cli

runner = CliRunner()
current_dir = os.path.dirname(__file__)


@given('a xpaths file named "{xpaths_filename}"')
def step_given_xpaths_file(context, xpaths_filename):
    context.xpaths_file = xpaths_filename


@given('a HTML file named "{page_filename}"')
def step_and_filename_of_html_page(context, page_filename):
    context.page = page_filename


@then('scraped data should match "{output_filename}"')
def step_impl(context, output_filename):
    result = runner.invoke(scraper.cli.main, [
        '--file', os.path.join(current_dir, context.xpaths_file),
        '--page', os.path.join(current_dir, context.page)])
    output = json.load(open(os.path.join(current_dir, output_filename)))
    assert json.loads(result.output) == output
