virtualenv venv
venv\Scripts\pip install -r requirements.txt
bower install
copy config.dev.py config.py
copy secretkeys_source.py secretkeys.py
echo Please update the secret key in secretkeys.py.
