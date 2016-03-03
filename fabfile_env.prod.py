"""
This file defines the host and directory for the CREM website
for deployment purposes.

This file must be named fabfile_env.py, so fabfile.py can import it.
However, do not version fabfile_env.py; instead version fabfile_env.dev.py,
fabfile_env.prod.py, etc., and copy the appropriate version to fabfile_env.py.
"""

HOSTS = ['goldmoth.com']
DIRECTORY = '/var/www/CREM'
USER = 'www-data'
DOMAIN = 'prod'
