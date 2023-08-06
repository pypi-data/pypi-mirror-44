import click

_global_test_options = [
    click.option('--debug/--no-debug', default=False, help='Debug mode'),
    click.option('--quiet/--no-quiet', default=False, help='Silent mode'),
]


def global_options(func):
    for option in reversed(_global_test_options):
        func = option(func)
    return func
