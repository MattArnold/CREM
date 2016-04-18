"""
Configuration file for CREM application.

There may be different versions of this file, for example:

config.dev.py for development,
config.prod.py for production,
etc.

These files will be under version control; config.py will not. Copy the
appropriate file to config.py.
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))

APP_ROOT = basedir
SECRET_KEY = ')J\x8dD\x94s\x00ac\x1a.\x171p\xab\xf8;\x05G\x0bc\x8a\xc0\x96'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
