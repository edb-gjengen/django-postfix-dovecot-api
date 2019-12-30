# Install
    apt install python-dev libmysqlclient-dev python-virtualenv
    python -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt

# Deploy
First you need to have your public key in `/home/gitdeploy/.ssh/authorized_keys` on the server and then you can do:

    fab deploy

# Inspiration:
- http://modoboa.readthedocs.org/
- https://github.com/lgunsch/django-vmail
