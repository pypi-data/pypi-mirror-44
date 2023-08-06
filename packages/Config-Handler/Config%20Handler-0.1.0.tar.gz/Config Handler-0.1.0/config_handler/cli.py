import click


@click.group(help=click.style("Handle config files in your projects the easy way", fg="green"))
@click.pass_context
def cli(ctx):
    """CLi starting point."""

    ctx.obj = {}


@cli.command(help=click.style("Hello World", fg="green"))
@click.pass_context
def hello_world(ctx):
    """__some_description__"""

    click.echo('Hello world')
