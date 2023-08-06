import click

from chaosloader.src.utils.decorators.common import global_options
from chaosloader.src.commands.validate import command as validate_commands


@click.group()
@global_options
def cli(debug, quiet):
    """Welcome to chaos loader cli"""
    pass


@click.command()
@click.pass_context
def run(context):
    """RUN ALL"""


"""
Add available commands here
"""
cli.add_command(validate_commands.validate, name="validate")
cli.add_command(run, name="run")
