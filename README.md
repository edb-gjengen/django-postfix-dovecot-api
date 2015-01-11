# Install
    apt install python-dev libmysqlclient-dev python-virtualenv
    virtualenv venv
    . venv/bin/activate
    pip install -r requirements

# Deploy
First you need to have your public key in /home/gitdeploy/.ssh/authorized_keys on the server.

Then, to deploy via login.neuf.no, add the following to your personal ~/.ssh/config

    Host lynx.neuf.no
      User gitdeploy
      ForwardAgent yes
      ProxyCommand ssh -W %h:%p login.neuf.no -l USERNAME

Then you can do

    fab deploy


# TODO
- Alias should only allow unique (source,destination) tuples

# TODO later
- Create domain dir for dovecot?
