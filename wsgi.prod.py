import sys
sys.path.insert(0, '/var/www/CREM')
activate_this = '/var/www/CREM/venv/bin/activate_this.py'
exec(compile(open(activate_this).read(), activate_this, 'exec'), dict(__file__=activate_this))

from app import app as application
