import logging
import sys

from contextlib import contextmanager as _contextmanager
from fabric.api import run, sudo, env, cd, prefix, lcd
from fabric.api import local as lrun

env.use_ssh_config = True
env.hosts = ['lynx.neuf.no']
env.project_path = '/var/www/neuf.no/django-postfix-dovecot-api'
env.user = 'gitdeploy'
env.activate = 'source {}/venv/bin/activate'.format(env.project_path)


@_contextmanager
def virtualenv():
    with cd(env.project_path):
        with prefix(env.activate):
            yield


def __git_validate_clean():
    with lcd(env.project_path):
        if lrun('git diff-files', capture=True) != '':
            logging.error("Your git-tree isn't clean! Commit your changes before deploying.")
            sys.exit(1)


def test():
    lrun("python manage.py test dpdapi")


def commit():
    lrun("git add -p && git commit")


def push():
    lrun("git push")


def prepare_deploy():
    test()
    commit()
    push()


def gitstatus():
    # __git_validate_clean()
    with virtualenv():
        # Get source
        run('git branch -v')


def deploy():
    # __git_validate_clean()
    with virtualenv():
        run('git pull')  # Get source
        run('pip install -r requirements.txt')  # install deps in virtualenv
        run('umask 022; python manage.py collectstatic --noinput')  # Collect static
        run('python manage.py migrate')  # Run DB migrations

    # Reload gunicorn
    sudo('/etc/init.d/gunicorn reload', shell=False)
