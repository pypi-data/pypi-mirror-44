import click

from kontrctl.commands import add_all_commands
from kontrctl.config import AppConfig
from kontrctl.log_config import load_logger
from kontrctl.version import KONTRCTL_VERSION


@click.group(help='Kontr portal Cli tool')
@click.version_option(KONTRCTL_VERSION)
@click.pass_context
def cli_main(ctx):
    import os
    if os.getenv('KONTR_LOG'):
        load_logger()
    ctx.obj = AppConfig()


add_all_commands(cli_main)


if __name__ == '__main__':
    cli_main(None)
