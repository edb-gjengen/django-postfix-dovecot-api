import os

from fabric import Connection
from invoke import task


@task()
def deploy(c):
    """Make sure proxy_user is set to your neuf username."""
    project_path = '/var/www/neuf.no/django-postfix-dovecot-api'
    proxy_user = os.getenv('DEPLOY_USER', os.getenv('USER'))

    c = Connection(host='gitdeploy@lynx.neuf.no', gateway=Connection('login.neuf.no', user=proxy_user))

    with c.cd(project_path), c.prefix('source {}/venv/bin/activate'.format(project_path)):
        c.run('git pull')  # Get source
        c.run('pip install -r requirements.txt')  # install deps in virtualenv
        c.run('umask 022; python manage.py collectstatic --noinput')  # Collect static
        c.run('python manage.py migrate')  # Run DB migrations

    # Reload mxapi.neuf.no
    c.sudo('/usr/bin/supervisorctl pid mxapi.neuf.no | xargs kill -HUP', shell=False)
