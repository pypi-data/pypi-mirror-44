import click
import json

from kontrctl.commands.submission_files import cli_submission_files
from kontrctl.config import AppConfig, Remote
from kontrctl.utils import helpers

cli_submissions = click.Group('submissions', help='Submissions management')

cli_submissions.add_command(cli_submission_files)


def remove_none(**params):
    new_params = {}
    for (k, v) in params.items():
        if v is not None:
            new_params[k] = v
    return new_params


@cli_submissions.command('list', help='List all submissions')
@click.option('-r', '--remote', required=False, help='Sets remote')
@click.option('-c', '--course', required=False, help='Sets course')
@click.option('-p', '--project', required=False, help='Sets project')
@click.option('-u', '--user', required=False, help='Sets user')
@click.option('-i', '--ids', required=False, is_flag=True, help='Get just ids')
@click.option('-s', '--state', required=False, help='Get submissions by state')
@click.option('-R', '--result', required=False, help='Get submissions by result')
@click.option('-P', '--points', required=False, help='Get points by expression (example: p > 3.0)')
@click.option('-C','--cols', required=False, help='Show just provided columns, separator is ;')
@click.option('--t-format', required=False, help='Table formats (default simple), look at the tabular projects for more')
@click.pass_obj
def cli_submissions_list(obj: AppConfig, remote=None, **kwargs):
    params = remove_none(**kwargs)
    remote: Remote = helpers.get_remote(obj, remote)
    submissions = remote.kontr_client.submissions.list(params=kwargs)
    params = ['id', 'created_at', 'result', 'points', 'state', 'user.username', 
    'course.codename', 'project.codename']
    submissions = helpers.filter_submissions(submissions, **kwargs)
    helpers.generic_list(submissions, options=kwargs, params=params)


@cli_submissions.command('read', help='Get a submission info')
@click.option('-r', '--remote', required=False, help='Sets remote')
@click.argument('sid', required=False)
@click.pass_obj
def cli_submissions_read(obj: AppConfig, remote, sid: str):
    remote: Remote = helpers.get_remote(obj, remote)
    submission = helpers.get_submission(remote, sid)
    if submission:
        helpers.entity_printer(submission)
    else:
        print("There are no submissions for you.")


@cli_submissions.command('stats', help='Get a submission stats')
@click.option('-r', '--remote', required=False, help='Sets remote')
@click.argument('sid', required=False)
@click.pass_obj
def cli_submissions_read(obj: AppConfig, remote, sid: str):
    remote: Remote = helpers.get_remote(obj, remote)
    submission = helpers.get_submission(remote, sid)
    if submission:
        print(json.dumps(submission.stats().json(), indent=4))
    else:
        print("There are no submissions for you.")


@cli_submissions.command('rm', help='Delete submission')
@click.option('-r', '--remote', required=False, help='Sets remote')
@click.argument('sid', required=False)
@click.pass_obj
def cli_submissions_delete(obj: AppConfig, remote, sid: str):
    remote: Remote = helpers.get_remote(obj, remote)
    print(f"Removing submission: {sid}")
    submission = helpers.get_submission(remote, sid)
    submission.delete()


@cli_submissions.command('cancel', help='Cancel submission')
@click.option('-r', '--remote', required=False, help='Sets remote')
@click.argument('sid', required=False)
@click.pass_obj
def cli_submissions_cancel(obj: AppConfig, remote, sid: str):
    remote: Remote = helpers.get_remote(obj, remote)
    print(f"Canceling submission: {sid}")
    submission = helpers.get_submission(remote, sid)
    submission.cancel()


@cli_submissions.command('resubmit', help='Resubmit submission')
@click.option('-r', '--remote', required=False, help='Sets remote')
@click.argument('sid', required=False)
@click.pass_obj
def cli_submissions_resubmit(obj: AppConfig, remote, sid: str):
    remote: Remote = helpers.get_remote(obj, remote)
    print(f"Resubmitting submission: {sid}")
    submission = helpers.get_submission(remote, sid)
    submission.resubmit()