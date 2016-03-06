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

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SCHEDULE_URL = 'https://docs.google.com/spreadsheets/d/1WFOl4XmKqsfvPQz46d2gRzFZEYrqIBj9Urmgsj0sNq4/export?format=csv'
