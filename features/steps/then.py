import difflib
import json
import os.path

from behave import then
from nose.tools import assert_in, eq_

current_dir = os.path.dirname(__file__)


class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values

    reference: https://github.com/hughdbrown/dictdiffer
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.current_keys, self.past_keys = [
            set(d.keys()) for d in (current_dict, past_dict)
        ]
        self.intersect = self.current_keys.intersection(self.past_keys)

    def added(self):
        return self.current_keys - self.intersect

    def removed(self):
        return self.past_keys - self.intersect

    def changed(self):
        return set(o for o in self.intersect
                   if self.past_dict[o] != self.current_dict[o])

    def __str__(self):
        print('\n'.join('Added:   ' + self.added(),
                        'Removed: ' + self.removed(),
                        'Changed: ' + self.changed()))


@then('display an informative file not found message')
def step_display_file_not_found(context):
    assert_in('"-P" / "--page": Could not open file', context.output)
    assert_in('oops.html: No such file or directory', context.output)


@then('the output should match "{output}"')
def step_match_output(context, output):
    eq_(context.output.strip(), output.strip())


@then('the output should match the file "{file_}"')
def step_output_should_match_file(context, file_):
    with open(os.path.join(current_dir, file_)) as output:
        if file_.endswith('.json'):
            context.output = json.loads(context.output)
            output = json.load(output)
            try:
                eq_(context.output, output)
            except AssertionError:
                print(str(DictDiffer(context.output, output)))
                raise

        else:
            context = list(map(str.strip, context.output.splitlines()))
            expected_result = list(map(str.strip, output.readlines()))
            try:
                eq_(context, expected_result)
            except AssertionError:
                d = difflib.Differ()
                for line in d.compare(context, expected_result):
                    print(line)
                raise


@then('there should be no output')
def step_no_output(context):
    eq_(context.output, '')


@then('display the XPath with a pointer below at the 12th character')
def step_xpath_point2_12th_char(context):
    lines = context.output.splitlines()
    eq_(lines[0], context.xpath)
    eq_(lines[1].find('^'), 11)
