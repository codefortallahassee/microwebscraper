import click
import lxml.cssselect


@click.command()
@click.argument('css_selector')
def main(css_selector):
    try:
        click.echo(lxml.cssselect.CSSSelector(css_selector).path)
    except lxml.cssselect.SelectorSyntaxError as e:
        name = e.__class__.__name__
        click.echo(click.style(name + ': ', fg='red', bold=True) + str(e))

if __name__ == '__main__':
    main()
