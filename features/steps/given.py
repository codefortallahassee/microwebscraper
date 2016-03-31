from behave import given


@given('a configuration file "{cfg_file}"')
def step_given_cfg_file(context, cfg_file):
    context.cfg_file = cfg_file


@given('a HTML page file "{page}"')
def step_given_html_page(context, page):
    context.page = page


@given('a XPath expression "{xpath}"')
def step_xpath_expr(context, xpath):
    context.xpath = xpath
