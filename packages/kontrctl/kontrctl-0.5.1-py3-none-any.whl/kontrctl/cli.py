import logging

import click
import kontr_api

import kontrctl
from kontrctl import log_config
from kontrctl.commands import add_all_commands
from kontrctl.config import AppConfig

log = logging.getLogger('kontrctl.cli')


@click.group(help='Kontr portal Cli tool')
@click.version_option(kontrctl.__version__)
@click.pass_context
def cli_main(ctx=None):
    import os
    if os.getenv('KONTR_LOG'):
        log_config.load_logger()
    log.info(f"KONTRCTL Version: {kontrctl.__version__} "
             f"KONTR-API Version: {kontr_api.__version__}")
    ctx.obj = AppConfig()


add_all_commands(cli_main)

if __name__ == '__main__':
    cli_main()
