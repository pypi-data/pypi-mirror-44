import click


@click.group(help=click.style("Extended functionalities and better control over Python\'s built-in print function", fg="green"))
@click.pass_context
def cli(ctx):
    """CLi starting point."""

    ctx.obj = {}


@cli.command(help=click.style("Hello World", fg="green"))
@click.pass_context
def hello_world(ctx):
    """__some_description__"""

    click.echo('Hello world')
