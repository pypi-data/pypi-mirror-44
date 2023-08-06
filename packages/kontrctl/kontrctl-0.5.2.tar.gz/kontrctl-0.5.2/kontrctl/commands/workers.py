import click

from kontrctl.config import AppConfig, Remote
from kontrctl.utils import helpers

cli_workers = click.Group('workers', help='Workers management')


@cli_workers.command('list', help='List all workers')
@click.option('-r', '--remote', required=False, help='Sets remote')
@click.pass_obj
def cli_workers_list(obj: AppConfig, remote):
    remote: Remote = helpers.get_remote(obj, remote)
    workers = remote.kontr_client.workers.list()
    helpers.generic_list(workers, params=['id', 'codename', 'state', 'url'])


@cli_workers.command('read', help='Get a worker info')
@click.option('-r', '--remote', required=False, help='Sets remote')
@click.argument('codename')
@click.pass_obj
def cli_workers_read(obj: AppConfig, remote, codename: str):
    remote: Remote = helpers.get_remote(obj, remote)
    helpers.generic_read(remote.kontr_client.workers, codename)


@cli_workers.command('status', help='Get a worker status')
@click.option('-r', '--remote', required=False, help='Gets a worker status')
@click.argument('codename')
@click.pass_obj
def cli_workers_status(obj: AppConfig, remote, codename: str):
    remote: Remote = helpers.get_remote(obj, remote)
    worker = helpers.read_helper(remote.kontr_client.workers, codename)
    status = worker.status.read()
    helpers.entity_printer(status)


@cli_workers.command('delete', help='Delete worker')
@click.option('-r', '--remote', required=False, help='Sets remote')
@click.argument('codename')
@click.pass_obj
def cli_workers_delete(obj: AppConfig, remote, codename: str):
    remote: Remote = helpers.get_remote(obj, remote)
    print(f"Removing worker: {codename}")
    remote.kontr_client.workers.delete(codename)


@cli_workers.command('edit', help='Edit worker')
@click.option('-r', '--remote', required=False, help='Sets remote')
@click.argument('codename')
@click.pass_obj
def cli_workers_edit(obj: AppConfig, remote, codename: str):
    remote: Remote = helpers.get_remote(obj, remote)
    helpers.generic_edit(remote.kontr_client.workers, codename)


@cli_workers.command('create', help='Create worker')
@click.option('-r', '--remote', required=False, help='Sets remote')
@click.option('-n', '--name', prompt=True, required=False, help='Name of the worker')
@click.option('-U', '--url', required=False, help='Url')
@click.option('-P', '--portal_secret', required=False, help='Portal secret')
@click.option('-T', '--tags', required=False, help='Tags')
def cli_workers_create(obj, remote, **kwargs):
    remote: Remote = helpers.get_remote(obj, remote)
    helpers.generic_create(remote.kontr_client.workers.create, **kwargs)

