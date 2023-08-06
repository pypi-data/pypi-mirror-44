import json
from pathlib import Path

import click
from kontr_api.resources import Submission

from kontrctl.config import AppConfig, Remote
from kontrctl.utils import helpers

cli_submission_files = click.Group('files', help='Submission files management')


def general_source_getter(submission, entity_name, path, out):
    client = getattr(submission, entity_name)
    if path is None:
        out = out or '.'
        out = Path(out) / f"{submission['id']}-{entity_name}.zip"
        client.download(out)
        print(f"Files downloaded: {out}")
    else:
        file_content = client.content(path)
        print(file_content)


@cli_submission_files.command('sources-tree', help='Get submission sources tree')
@click.option('-r', '--remote', required=False, help='Sets remote')
@click.argument('sid', required=False)
@click.pass_obj
def cli_submission_files_sources(obj: AppConfig, remote, sid: str):
    remote: Remote = helpers.get_remote(obj, remote)
    submission = helpers.get_submission(remote, sid)
    print(json.dumps(submission.sources.tree(), indent=4))


@cli_submission_files.command('results-tree', help='Get results tree')
@click.option('-r', '--remote', required=False, help='Sets remote')
@click.argument('sid', required=False)
@click.pass_obj
def cli_submission_files_sources(obj: AppConfig, remote, sid: str):
    remote: Remote = helpers.get_remote(obj, remote)
    submission = helpers.get_submission(remote, sid)
    print(json.dumps(submission.results.tree(), indent=4))


@cli_submission_files.command('test-files-tree', help='Get results tree')
@click.option('-r', '--remote', required=False, help='Sets remote')
@click.argument('sid', required=False)
@click.pass_obj
def cli_submission_files_sources(obj: AppConfig, remote, sid: str):
    remote: Remote = helpers.get_remote(obj, remote)
    submission = helpers.get_submission(remote, sid)
    print(json.dumps(submission.test_files.tree(), indent=4))


@cli_submission_files.command('sources', help='Get submission sources')
@click.option('-r', '--remote', required=False, help='Sets remote')
@click.option('-o', '--out', required=False, help='Set out path')
@click.option('-P', '--path', required=False, help='File path')
@click.argument('sid', required=False)
@click.pass_obj
def cli_submission_files_sources(obj: AppConfig, remote, sid: str, out=None, path: str = None):
    remote: Remote = helpers.get_remote(obj, remote)
    submission = helpers.get_submission(remote, sid)
    general_source_getter(submission, 'sources', path=path, out=out)


@cli_submission_files.command('results', help='Get submission results')
@click.option('-r', '--remote', required=False, help='Sets remote')
@click.option('-o', '--out', required=False, help='Set out path')
@click.option('-P', '--path', required=False, help='File path')
@click.argument('sid', required=False)
@click.pass_obj
def cli_submission_files_results(obj: AppConfig, remote, sid: str, out=None, path: str = None):
    remote: Remote = helpers.get_remote(obj, remote)
    submission = helpers.get_submission(remote, sid)
    general_source_getter(submission, 'results', path=path, out=out)


@cli_submission_files.command('test-files', help='Get submission results')
@click.option('-r', '--remote', required=False, help='Sets remote')
@click.option('-o', '--out', required=False, help='Set out path')
@click.option('-P', '--path', required=False, help='File path')
@click.argument('sid', required=False)
@click.pass_obj
def cli_submission_files_test_files(obj: AppConfig, remote, sid: str, out=None, path: str = None):
    remote: Remote = helpers.get_remote(obj, remote)
    submission = helpers.get_submission(remote, sid)
    general_source_getter(submission, 'test_files', path=path, out=out)
