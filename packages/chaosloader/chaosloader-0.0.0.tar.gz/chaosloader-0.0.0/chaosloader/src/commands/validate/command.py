import click

from chaosloader.src.utils.decorators.common import global_options
from chaosloader.src.commands.validate.environment.environment import environment
from chaosloader.src.commands.validate.environment.config import config


@click.group()
@click.pass_context
@global_options
def validate(context, debug, quiet):
    """Validate set of sub commands"""
    pass


validate.add_command(environment, name="environment")
validate.add_command(config, name="config")
