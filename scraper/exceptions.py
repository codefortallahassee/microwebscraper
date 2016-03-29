import json
import re

import click
import jsonschema
import lxml.etree
import requests


class ScraperException(Exception):
    """An error occured while trying to scrape the web page."""

    def __init__(self, *args, **kwargs):
        self.disp_width = 76
        self.value = kwargs.pop('key', None)
        self.value = kwargs.pop('value', None)
        self.filename = kwargs.pop('filename', None)
        try:
            self.err_name = self.args[0][0].__name__
        except IndexError:
            self.err_name = None
        try:
            self.msg = str(self.args[0][1])
        except IndexError:
            self.msg = ''
        super(ScraperException, self).__init__(*args, **kwargs)

    def __str__(self):
        name = self.__class__.__name__
        if self.err_name and self.err_name != name:
            name += '({})'.format(self.err_name)
        return name + ': ' + self.mesg

    def echo(self):
        """Prints an easy-to-read formatted/colorized error message"""
        self.point2error()
        name = self.style_class_and_exc_name()
        click.echo(name + ': ' + click.style(self.msg, fg='white'))
        if self.key is not None:
            click.secho('Exception ocurred in key: {!r}'.format(self.key))

    def style_class_and_exc_name(self):
        """Formats & colorizes the parent/child exception names"""
        name = click.style(self.__class__.__name__, fg='red', bold=True)
        if self.err_name and self.err_name != self.__class__.__name__:
            name += click.style('({})'.format(self.err_name), fg='yellow')
        return name

    def point2error(self):
        """Prints a colored pointer showing where error first occured"""
        try:
            visible_text, column = self.get_error_position()
        except AttributeError:
            return

        pointer = ''
        start_pos, stop_pos = None, None
        if column > self.disp_width and column < len(visible_text):
            start_pos = column - int(self.disp_width / 2) - 1
            stop_pos = start_pos + self.disp_width
            visible_text = visible_text[start_pos:stop_pos]
        pointer = ' ' * (column - 1) + '^'
        click.secho(visible_text + '\n' + pointer, fg='yellow', bold=True)


class FailedToParseHTML(ScraperException, lxml.etree.ParseError):
    """Error while parsing HTML document with lxml

    If you are getting this error you may want to consider using a
    different parser. Three differnt parsers are supported in lxml:
    lxml.html, soupparser & html5parser.   soupparser & html5parser
    have better support for tag soup.

    Reference: http://lxml.de/parsing.html#parsing-html
    """


class HTMLEncodingIssue(UnicodeDecodeError):
    """UnicodeDecodeError: Error parsing the HTML document with lxml

    If you are getting this error you may want to conider using
    soupparser if you are not already using it since it has the best
    support for encoding detection with HTML pages that do not
    (correctly) declare their encoding.

    Reference: http://lxml.de/elementsoup.htm
    """


class FailedToLoadWebPage(ScraperException, requests.RequestException):
    """RequestException: Error retrieving HTML from a URL using requests.get()

    Reference: http://docs.python-requests.org/en/master/api
    """


class RequestsTypeError(ScraperException, TypeError):
    """RequestFailed: Wrong argument types supplied to requests module

    Reference: http://docs.python-requests.org/en/master/api
    """


class InvalidScraperConfig(ScraperException, jsonschema.ValidationError):
    """Scraper configuration failed to validate against the JSON schema

    References:
        - scraperschema.json
        - http://json-schema.org
        - http://spacetelescope.github.io/understanding-json-schema/
    """

    def echo(self):
        """Outputs and colorizes the error message for easy reading

        Only displays the colors if colorama is installed
        """
        new_paragraph = True
        for line in self.msg.splitlines():
            if not line.strip():
                new_paragraph = True
                click.echo()
            elif new_paragraph:
                click.secho(line, fg='yellow', bold=True)
                new_paragraph = False
            else:
                click.secho(line, fg='yellow')
        click.echo('\n' + self.style_class_and_exc_name())


class DataIsNotJSON(ScraperException, json.JSONDecodeError):
    """Data being deserialized is not a valid JSON document"""

    error_position = re.compile(r'line\s(\d+)\s+column\s(\d+)')

    def get_error_position(self):
        match = self.__class__.error_position.search(self.msg)
        if match:
            line, column = map(int, match.groups())
            return self.value.splitlines()[line - 1], column


class InvalidXPathExpression(ScraperException, lxml.etree.XPathSyntaxError):
    """Not a valid XPath 1.0 expression"""

    xpath_step_sep_re = re.compile(r'(?<!\\)/{1,2}')

    def _test_xpath_fragment(self, xpath_fragment, prev_step):
        """On XPath Syntax Error return end position of previous XPath expr"""
        try:
            lxml.etree.XPath(xpath_fragment)
        except lxml.etree.XPathSyntaxError:
            xpath = self.value
            while prev_step is not None and xpath[prev_step] == '/':
                prev_step = None if prev_step == len(xpath) else prev_step + 1
            return prev_step

    def get_error_position(self):
        """Returns XPath character position of 1st XPath StepExpr failure

        StepExpr (("/" |  "//") StepExpr)*
        https://www.w3.org/2002/11/xquery-xpath-applets/xpath-bnf.html
        """
        xpath = self.value
        regex = self.__class__.xpath_step_sep_re
        step_ends = [i.start() for i in regex.finditer(xpath)]
        if not step_ends:
            return

        if step_ends[0] == 0:
            del step_ends[0]

        last_step = 0
        for end_pos in step_ends + [None]:
            result = self._test_xpath_fragment(xpath[:end_pos], last_step)
            if result:
                return self.value, result + 1
            last_step = end_pos
