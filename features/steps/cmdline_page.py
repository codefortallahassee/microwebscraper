import os

from nose.tools import assert_equals, assert_in
from behave import given, when, then
from click.testing import CliRunner

import scraper.cli

runner = CliRunner()
current_dir = os.path.dirname(__file__)


# Scenario: format & display HTML from a file

@then('format/tidy the HTML and output it to the console')
def step_tidy_html(context):
    context.result = runner.invoke(scraper.cli.main, [
        '--page', os.path.join(current_dir, context.page),
        '--tidy']).output


@then('the output format should match "{output_filename}"')
def step_output_fmt_should_match(context, output_filename):
    output = open(os.path.join(current_dir, output_filename)).read()
    assert_equals(context.result, output)

# Scenario: gracefully handle non-existant HTML file


@when('the file can not be found')
def step_file_not_found(context):
    context.result = runner.invoke(scraper.cli.main, [
        '--page', os.path.join(current_dir, context.page)]).output


@then('display a friendly, informative file not found message')
def step_display_file_not_found_msg(context):
    assert_in('"-P" / "--page": Could not open file', context.result)
    assert_in('oops.html: No such file or directory', context.result)
