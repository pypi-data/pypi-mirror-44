import click

from chaosloader.src.utils.decorators.common import global_options


@click.command()
@click.pass_context
@global_options
def environment(context, debug, quiet):
    """Validate generated .env files"""
    click.echo("command apply works!")
