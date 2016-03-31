import json
import os.path

from behave import then
from nose.tools import assert_in, eq_

current_dir = os.path.dirname(__file__)


@then('display an informative file not found message')
def step_display_file_not_found(context):
    assert_in('"-P" / "--page": Could not open file', context.output)
    assert_in('oops.html: No such file or directory', context.output)


@then('the output should match "{output}"')
def step_match_output(context, output):
    eq_(context.output.strip(), output.strip())


@then('the output should match the file "{file_}"')
def step_output_should_match_file(context, file_):
    output = open(os.path.join(current_dir, file_))
    if file_.endswith('.json'):
        context.output = json.loads(context.output)
        output = json.load(output)
    else:
        output = output.read()
    eq_(context.output, output)


@then('there should be no output')
def step_no_output(context):
    eq_(context.output, '')


@then('display the XPath with a pointer below at the 12th character')
def step_xpath_point2_12th_char(context):
    lines = context.output.splitlines()
    eq_(lines[0], context.xpath)
    eq_(lines[1].find('^'), 11)
