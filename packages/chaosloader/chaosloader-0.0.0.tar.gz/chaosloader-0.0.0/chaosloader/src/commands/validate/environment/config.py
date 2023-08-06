import click

from chaosloader.src.utils.decorators.common import global_options


@click.command()
@click.pass_context
@global_options
def config(context, debug, quiet):
    """Validate .env.json config files"""
    click.echo("command apply works!")
