"""
Deploys the website. See fabfile_env.py for configuration parameters.
"""

from fabric.api import local, sudo, env, settings, cd
import fabric.operations
import fabfile_env

env.hosts = fabfile_env.HOSTS


def domain():
    print fabfile_env.DOMAIN


def pull_changes():
    with cd(fabfile_env.DIRECTORY):
        sudo('git pull', user=fabfile_env.USER)
        sudo('cp wsgi.%s.py wsgi.py' % fabfile_env.DOMAIN,
             user=fabfile_env.USER)
        sudo('cp config.%s.py config.py' % fabfile_env.DOMAIN,
             user=fabfile_env.USER)


def update_packages():
    with cd(fabfile_env.DIRECTORY):
        sudo('source venv/bin/activate && pip install -r requirements.txt',
             user=fabfile_env.USER)


def restart():
    sudo('service apache2 restart')


def deploy():
    print 'Deploying to %s' % fabfile_env.DOMAIN
    pull_changes()
    update_packages()
    restart()
