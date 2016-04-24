import bcrypt
import binascii
import urllib
import os
import logging
from logging.handlers import RotatingFileHandler
import urlparse
import json
import datetime
from collections import defaultdict

from app import app
from app import db
from app.models import Convention, Event, Track, Room, RoomGroup, Timeslot, DataLoadError
from app.models import User
from flask import jsonify, request, render_template, url_for, redirect, session, abort
from flask.ext.login import LoginManager, login_required
from flask.ext.login import login_user, logout_user, current_user
from wtforms import Form, StringField
from wtforms.validators import DataRequired
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.exc import SQLAlchemyError

import refresh_data

# Set up logging.
if not app.debug:
    if 'APP_ROOT' in app.config:
        log_fname = os.path.join(app.config['APP_ROOT'], 'crem.log')
    else:
        log_fname = 'crem.log'
    filehandler = logging.handlers.RotatingFileHandler(log_fname, 'a',
                                                       100000, 10)
    filehandler.setLevel(logging.INFO)
    filehandler.setFormatter(logging.Formatter(
        '%(asctime)s %(process)-6s %(levelname)-8s: %(funcName)s: %(message)s'))
    app.logger.addHandler(filehandler)
    app.logger.setLevel(logging.INFO)


def generate_csrf_token():
    """
    Generate a CSRF token that can be included in forms, and checked in
    methodes which accept POST data.
    """
    if '_csrf_token' not in session:
        session['_csrf_token'] = binascii.hexlify(os.urandom(24))
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token


# Setup security.
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(user_id):
    try:
        return User.query.get(user_id)
    except SQLAlchemyError, e:
        app.logger.error('Unable to query for user in user_loader(): %s' % e)
        abort(500)


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])


class ImportForm(Form):
    source_url = StringField('source_url', validators=[DataRequired()])


def jsdate2py(s):
    """
    Converts a string to a Python datetime object. Returns None if the string
    cannot be converted. An example of the string is:

    2016-4-29T:20
    """
    try:
        parts = s.strip().split('T:')
        dateparts = parts[0].split('-')
        year = int(dateparts[0])
        month = int(dateparts[1])
        day = int(dateparts[2])
        hour = int(parts[1])
    except Exception:
        return None
    return datetime.datetime(year, month, day, hour, 0, 0)


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/convention.json', methods=['GET', 'POST'])
def convention():
    if request.method == 'GET':
        conventions = Convention.query.all()
        return jsonify(configs = [i.configs for i in conventions])
    else:
        content = request.json
        try:
            convention = Convention.query.one()
        except MultipleResultsFound:
            # Error: there should be one and only one convention record.
            return ('There is more than one convention record.', 500)
        convention.name = content['name']

        # Convert the start date to a Python datetime object.
        start_dt = jsdate2py(content['start_dt'])
        if start_dt is None:
            return ('Unable to parse the convention start date.', 500)
        convention.start_dt = start_dt

        # Convert the timeslot length from minutes to a timedelta object.
        convention.timeslot_length = datetime.timedelta(0, int(content['timeslot_length']) * 60)

        convention.number_of_timeslots = content['number_of_timeslots']

        # Update the database.
        try:
            db.session.add(convention)
            db.session.commit()
        except SQLAlchemyError, e:
            return ('Error updating the convention record: %s' % e, 500)
        return ('Convention data successfully updated.', 200)

@app.route('/number_of_timeslots.json')
def number_of_timeslots():
    number_of_timeslots = Timeslot.query.count()
    return jsonify(number_of_timeslots = number_of_timeslots)

@app.route('/tracks.json')
def tracks():
    tracklist = Track.query.all()
    return jsonify(tracknames = [i.names for i in tracklist])

@app.route('/columns.json')
def columns():
    return jsonify(
        columns = {
        'eventnumber': {'id':'eventnumber','name':'#',},
        'title': {'id':'title','name':'Title',},
        'track': {'id':'track','name':'Track',},
        'start': {'id':'start','name':'Start',},
        'duration': {'id':'duration','name':'Duration',},
        'rooms': {'id':'rooms','name':'Room',},
        'type': {'id':'type','name':'Type',},
        'presenters': {'id':'presenters','name':'Program Participants',},
        'resources': {'id':'resources','name':'Resources',},
        'description': {'id':'description','name':'Description',},
        'comments': {'id':'comments','name':'Staff Comments',},
        'conflict': {'id': 'conflict','name':'Conflict',}
        })

@app.route('/eventlist.json')
def events():
    events = Event.query.all()

    # Index events by ID, prepare for conflict annotation
    events_by_id = {}
    for event in events:
        data = event.useroutput
        data['conflict'] = "<div class='noconflicticon'>OK</div>"
        events_by_id[event.id] = data

    # Collate events by timeslot+presenter and timeslot+room
    events_by_timeslot_and_presenter = defaultdict(list)
    events_by_timeslot_and_room = defaultdict(list)
    for event in events:

        # Ignore inactive events
        if not event.active:
            continue

        # Scan all timeslots for the event
        for timeslot in event.timeslots:

            # Collect this event into a timeslot:presenter bucket
            for presenter in event.presenters:
                key = '%s:%s' % (timeslot.id, presenter.id)
                events_by_timeslot_and_presenter[key].append(event.id)

            # Collect this event into a timeslot:room bucket
            for room in event.rooms:
                key = '%s:%s' % (timeslot.id, room.id)
                events_by_timeslot_and_room[key].append(event.id)

    # Annotate events with presenter conflicts
    for key, event_ids in events_by_timeslot_and_presenter.items():
        # If this timeslot & presenter appears in multiple events, all those
        # events are in conflict.
        if len(event_ids) > 1:
            for event_id in event_ids:
                events_by_id[event_id]['conflict'] = "<div class='conflicticon'>&nbsp;Participant</div>"

    # Annotate events with room conflicts
    for key, event_ids in events_by_timeslot_and_room.items():
        # If this timeslot & room appears in multiple events, all those
        # events are in conflict.
        if len(event_ids) > 1:
            for event_id in event_ids:
                if events_by_id[event_id]['conflict'] == "<div class='conflicticon'>&nbsp;Participant</div>":
                    events_by_id[event_id]['conflict'] += "<div class='conflicticon'>&nbsp;Room</div>"
                else:
                    events_by_id[event_id]['conflict'] = "<div class='conflicticon'>&nbsp;Room</div>"

    return jsonify(eventlist = events_by_id.values())

@app.route('/rooms.json', methods=['GET', 'POST'])
def rooms():
    if request.method == 'GET':
        roomlist = Room.query.all()
        return jsonify(rooms=[i.ui_rooms for i in roomlist])
    else:
        rooms = request.json
        for room in rooms:
            if 'id' not in room:
                db_room = Room()
            else:
                db_room = Room.query.get(room['id'])
            db_room.room_name = room['name']
            db_room.room_sq_ft = room['sq_ft']
            db_room.room_capacity = room['capacity']
            db_room.room_group_id = room['group_id']
            db.session.add(db_room)

        # Update the database.
        try:
            db.session.commit()
        except SQLAlchemyError, e:
            return ('Error updating the room records: %s' % e, 500)
        return ('Room configs successfully updated.', 200)

@app.route('/room_groups.json')
def room():
    roomgrouplist = RoomGroup.query.all()
    return jsonify(
        room_groups = [i.ui_room_groups for i in roomgrouplist],
        )

@app.route('/configs.json')
def combined_info():
    convention = Convention.query.first()
    tracks = Track.query.all()
    rooms = Room.query.all()
    room_groups = RoomGroup.query.all()
    return jsonify(
        {
            "convention": {
                "name": convention.name,
                "start_dt": convention.start_dt.strftime(convention.datetime_format),
                "timeslot_length": int(convention.timeslot_duration.total_seconds()/60),
                "number_of_timeslots": convention.number_of_timeslots,
            },
            "tracks": [i.names for i in tracks],
            "rooms": [{"name": i.room_name,
                       "capacity": i.room_capacity,
                       "sq_ft": i.room_sq_ft,
                       "group_id": i.room_group_id,
                       "id": i.id,
                       # TODO: rename this to bookings and make values returned useful.
                       "available_timeslots": [{"name": j.timeslot.name,
                                                "index": j.timeslot.timeslot_index
                                                }
                                               for j in i.bookings],
                       "suitable_events": [{"id": j.id,
                                            "title": j.title
                                            }
                                           for j in i.suitable_events]
                       }
                      for i in rooms],
            "room_groups": [i.ui_room_groups for i in room_groups]
        }
    )


@app.route('/refresh-database', methods=['GET', 'POST'])
@login_required
def refresh_database():
    error = None
    form = ImportForm(request.form)
    if request.method == 'POST' and form.validate():
        # Check the CSRF token.
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

        url = form.source_url.data.strip()
        if not url:
            app.logger.info('No URL specified')
            error = 'The URL for schedule document was not specified'
        else:
            app.logger.info('The user specified the URL %s' % url)

            # Make sure the URL has the right suffix to export in CSV form.
            urlparts = urlparse.urlparse(url)
            path = urlparts.path
            if path.lower().endswith('/pub'):
                path = path[:-4]
            elif path.endswith('/'):
                path = path[:-1]
            newurl = '%s://%s%s/pub?output=csv' % (urlparts.scheme, urlparts.netloc,
                                                   path)
            app.logger.info('The new URL is %s' % newurl)

            try:
                result = urllib.urlretrieve(newurl)
            except Exception, e:
                error = 'Unable to read the schedule document: %s' % e
            else:
                # Refresh the database and delete the temporary export file.
                fname = result[0]
                refresh_data.refresh_data(fname)
                os.remove(fname)

                # Show any errors which occurred.
                return redirect('/show-database-errors')
    return render_template('refresh_database.html', form=form, error=error)


@app.route('/show-database-errors')
@login_required
def show_database_errors():
    # Display errors and warnings that occurred when refreshing the database.
    load_errors = DataLoadError.query.order_by(DataLoadError.line_num).all()
    return render_template('load_errors.html', load_errors=load_errors)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # Check the CSRF token.
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

        try:
            user = User.query.get(form.username.data)
        except SQLAlchemyError, e:
            app.logger.error('Unable to query for user in login(): %s' % e)
            abort(500)
        password = form.password.data
        if user and bcrypt.hashpw(password.encode('utf-8'), user.encpwd.encode('utf-8')).decode() == user.encpwd:
            user.authenticated = True
            db.session.add(user)
            try:
                db.session.commit()
            except SQLAlchemyError, e:
                app.logger.error('Unable to commit user authentication in login(): %s' % e)
                abort(500)
            login_user(user, remember=True)
            return redirect('/')
        else:
            error = 'the user name or password are incorrect.'
    return render_template('login.html', form=form, error=error)


@app.route('/logout/', methods=["GET"])
def logout():
    user = current_user
    if user.get_id():
        user.authenticated = False
        db.session.add(user)
        try:
            db.session.commit()
        except SQLAlchemyError, e:
            app.logger.error('Unable to commit user authentication in logout(): %s' % e)
            abort(500)
        logout_user()
    return redirect('/')
