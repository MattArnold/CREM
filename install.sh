python virtualenv.py venv
venv/bin/pip install -r requirements.txt
bower install
cp config.dev.py config.py
cp secretkeys_source.py secretkeys.py
echo Please update the secret key in secretkeys.py.
