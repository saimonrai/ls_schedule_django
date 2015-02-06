#!/usr/bin/env python
from fabric.api import local
from fabric.context_managers import settings, cd, prefix
from fabric.contrib.console import confirm
from fabric.operations import sudo, run
from fabric.state import env
from fabric.utils import abort
from fabric import colors

__author__ = 'Saimon Rai'
__copyright__ = 'Copyright 2013 Poolsidelabs Inc.'

env.hosts = ['54.254.239.46']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/default__saimonraigmail.cer'

PROJECT_DIR = '/usr/local/src/ls_schedule'
PYTHON_EXEC = '/usr/local/venv/ls_schedule/bin/python'
PIP_EXEC = '/usr/local/venv/ls_schedule/bin/pip'


def test():
    """
    Run unit-tests.
    """
    print(colors.green("Running unit tests..."))
    with settings(warn_only=True):
        result = local('./manage.py test', capture=False)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

def commit():
    """
    Commit changes.
    """
    print(colors.green("Committing changes..."))
    with settings(warn_only=True):
        result = local("git add -p && git commit")
    if result.failed and not confirm("Nothing to commit. Continue anyway?"):
        abort("Aborting at user request.")

def push():
    """
    Push changes to the git server.
    """
    print(colors.green("Pushing changes..."))
    local("git push")

def prepare_deploy():
    """
    Run tests; commit changes; push changes.
    """
    print(colors.green("Preparing deployment..."))
#    test() TODO: FIX ME
    commit()
    push()

def deploy():
    """
    Deploy the changes to the remote machines.
    """
#    prepare_deploy()

    print(colors.yellow("\nDeployment begins..."))
    print(colors.red("NOTE: Staged commits will NOT be pushed!\n"))

    with cd(PROJECT_DIR):
        print(colors.green("Pulling changes..."))
        run("git pull")

        print(colors.green("Installing python packages listed in the requirements file..."))
        run("{pip} install -r requirements.txt".format(pip=PIP_EXEC))

        print(colors.green("Syncing database..."))
        run("{python} manage.py syncdb".format(python=PYTHON_EXEC))

        print(colors.green("Collecting static files..."))
        sudo("{python} manage.py collectstatic --noinput".format(python=PYTHON_EXEC))

        print(colors.green("Installing cron jobs..."))
        run("{python} manage.py installtasks".format(python=PYTHON_EXEC))

        print(colors.green("Restarting gunicorn..."))
        sudo("service gunicorn-ls_schedule restart")

        print(colors.green("Restarting nginx..."))
        sudo("service nginx restart")

    print(colors.yellow("Deployment complete.\n"))


