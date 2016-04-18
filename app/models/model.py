from .. import db


# Associate multiple rooms to multiple events.
room_event = db.Table(
    'room_event',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('room_id', db.Integer, db.ForeignKey('room.id'))
)

# Associate multiple timeslots to multiple events.
timeslot_event = db.Table(
    'timeslot_event',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('timeslot_id', db.Integer, db.ForeignKey('timeslot.id'))
)

# Associates multiple presenters to multiple events.
presenter_event = db.Table(
    'presenter_event',
    db.Column(
        'event_id',
        db.Integer,
        db.ForeignKey('event.id', ondelete='CASCADE', onupdate='CASCADE')
    ),
    db.Column(
        'presenter_id',
        db.Integer,
        db.ForeignKey('presenter.id', ondelete='CASCADE', onupdate='CASCADE')
    )
)

room_suitability = db.Table(
    'room_suitability',
    db.Column(
        'eventtype_id',
        db.Integer,
        db.ForeignKey('eventtype.id', ondelete='CASCADE', onupdate='CASCADE')
    ),
    db.Column(
        'room_id',
        db.Integer,
        db.ForeignKey('room.id', ondelete='CASCADE', onupdate='CASCADE')
    )
)


class Track(db.Model):
    __tablename__ = 'track'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    uid = db.Column(db.String(), unique=True)
    email = db.Column(db.String(), unique=True)
    trackhead_first_name = db.Column(db.String())
    trackhead_last_name = db.Column(db.String())
    active = db.Column(db.Boolean(), default=True)
    events = db.relationship('Event', backref='track',
                             cascade='all, delete-orphan')

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.uid = email[:email.find('@')]

    def __repr__(self):
        return 'Track: %s' % self.name

    @property
    def names(self):
        """ Return only the names and uids of the tracks. """
        return {
            'name': self.name,
            'uid': self.uid
        }

    """
    The only reason CREM keeps staff email addresses in the
    database is so CREM can send emails. We will not
    include staff email addresses in any AJAX endpoints
    because all our staff understand each email
    begins with a track name, so they know how to contact
    each other already. Users = tracks = email addresses.
    If we expose them through an endpoint, the only value
    we provide would be for spam spiders to collect them.
    """


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    comments = db.Column(db.String())
    active = db.Column(db.Boolean(), default=True)
    track_id = db.Column(db.Integer(), db.ForeignKey('track.id'))
    rooms = db.relationship('Room',
                            secondary='room_event',
                            backref=db.backref('used_for_event'))
    eventtype_id = db.Column(db.Integer, db.ForeignKey('eventtype.id'))
    players = db.Column(db.Integer())
    roundTables = db.Column(db.Integer())
    longTables = db.Column(db.Integer())
    facilityRequest = db.Column(db.String())
    presenters = db.relationship(
        'Presenter',
        secondary=presenter_event,
        backref=db.backref('at_event'),
        passive_deletes=True
    )
    timeslots = db.relationship('Timeslot',
                                secondary='timeslot_event',
                                backref=db.backref('has_event'))
    duration = db.Column(db.Integer)  # The number of timeslots.
    convention_id = db.Column(db.Integer, db.ForeignKey('convention.id'))
    convention = db.relationship('Convention')
    fixed = db.Column(db.Boolean())

    def __repr__(self):
        return 'Event: %s' % self.title

    @property
    def useroutput(self):
        presenter_list = []
        for presenter in self.presenters:
            presenter_name = ('%s %s' % (presenter.first_name,
                                         presenter.last_name)).strip()
            presenter_list.append(presenter_name)

        room_list = []
        for room in self.rooms:
            room_name = ('%s' % (room.room_name,)).strip()
            room_list.append(room_name)

        # Find the index of the first timeslot for this event.
        timeslot_index = None
        for timeslot in self.timeslots:
            if not timeslot_index:
                timeslot_index = timeslot.timeslot_index
            elif timeslot.timeslot_index < timeslot_index:
                timeslot_index = timeslot.timeslot_index

        # Create the string representing the start datetime.
        if timeslot_index:
            timeslot_duration = self.convention.timeslot_duration
            start_dt = self.convention.start_dt + timeslot_duration * timeslot_index
            if self.convention.datetime_format:
                start_dt_str = start_dt.strftime(self.convention.datetime_format)
            else:
                start_dt_str = start_dt.strftime('%m/%d/%Y %I:%M %p')
        else:
            start_dt_str = ''

        return {
            'eventnumber': self.id,
            'title': self.title,
            'description': self.description,
            'comments': self.comments,
            'trackuid': self.track.uid,
            'track': self.track.name,
            'rooms': ', '.join(room_list),
            'event_type': self.event_type,
            'presenters': ', '.join(presenter_list),
            'start': start_dt_str,
            'duration': self.duration
        }


class EventType(db.Model):
    __tablename__ = 'eventtype'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    active = db.Column(db.Boolean(), default=True)
    events = db.relationship('Event', backref='event_type')


class Presenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    phone = db.Column(db.String())
    active = db.Column(db.Boolean(), default=True)
    presentations = db.relationship(
        'Event',
        secondary=presenter_event,
        backref=db.backref('presented_by', passive_deletes=True)
    )

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return '%s %s (%s)' % (self.first_name, self.last_name, self.email)


class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(50))
    room_sq_ft = db.Column(db.Integer)
    room_capacity = db.Column(db.Integer)
    room_group_id = db.Column(db.Integer, db.ForeignKey('room_group.id'))
    active = db.Column(db.Boolean(), default=True)
    bookings = db.relationship('RoomBooked', backref='room')

    suitable_events = db.relationship(
        'EventType',
        secondary=room_suitability,
        backref=db.backref('suitable_rooms'),
        passive_deletes=True
    )

    def __repr__(self):
        return 'Room: %s' % self.room_name

    @property
    def ui_rooms(self):
        return {
            'id': self.id,
            'name': self.room_name,
            'sq_ft': self.room_sq_ft,
            'capacity': self.room_capacity,
            'group_id': self.room_group_id,
            'suitable_events': self.suitable_events,
            # TODO: rename this to booked_timeslots.
            'available_timeslots': self.bookings
        }


class RoomGroup(db.Model):
    __tablename__ = 'room_group'
    id = db.Column(db.Integer, primary_key=True)
    room_group_name = db.Column(db.String(50))
    rooms = db.relationship('Room', backref='room_group',
                            cascade='all, delete-orphan')

    def __init__(self, room_group_name):
        self.room_group_name = room_group_name

    def __repr__(self):
        return 'Room Group: %s' % self.room_group_name

    @property
    def ui_room_groups(self):
        return self.room_group_name


class Convention(db.Model):
    __tablename__ = 'convention'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    start_dt = db.Column(db.DateTime)
    end_dt = db.Column(db.DateTime)
    date_format = db.Column(db.String(50))
    datetime_format = db.Column(db.String(50))
    url = db.Column(db.String())
    timeslot_duration = db.Column(db.Interval())
    number_of_timeslots = db.Column(db.Integer)
    active = db.Column(db.Boolean(), default=True)

    def __repr__(self):
        return self.name

    @property
    def configs(self):
        return {
            'name': self.name,
            'start_dt': str(self.start_dt),
            'end_dt': str(self.end_dt),
            'timeslot_length': int(self.timeslot_duration.total_seconds() / 60),
            'number_of_timeslots': self.number_of_timeslots,
        }


class Timeslot(db.Model):
    __tablename__ = 'timeslot'
    id = db.Column(db.Integer(), primary_key=True)
    timeslot_index = db.Column(db.Integer(), unique=True)  # 0-based.
    name = db.Column(db.String())
    rsvp_conflicts = db.Column(db.Integer())
    active = db.Column(db.Boolean(), default=True)
    room_bookings = db.relationship('RoomBooked', backref='timeslot')
    presenter_bookings = db.relationship('PresenterBooked', backref='timeslot')

    def __init__(self, timeslot_index):
        self.timeslot_index = timeslot_index


class PresenterBooked(db.Model):
    __tablename__ = 'presenter_booked'
    id = db.Column(db.Integer(), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    presenter_id = db.Column(db.Integer, db.ForeignKey('presenter.id'))
    timeslot_id = db.Column(db.Integer, db.ForeignKey('timeslot.id'))


class RoomBooked(db.Model):
    __tablename__ = 'room_booked'
    id = db.Column(db.Integer(), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    timeslot_id = db.Column(db.Integer, db.ForeignKey('timeslot.id'))


class DataLoadError(db.Model):
    __tablename__ = 'data_load_error'
    id = db.Column(db.Integer(), primary_key=True)
    error_level = db.Column(db.String(50))
    destination_table = db.Column(db.String(50))
    line_num = db.Column(db.Integer)
    error_msg = db.Column(db.String(50))
    error_dt = db.Column(db.DateTime)


class User(db.Model):
    __tablename__ = 'app_user'

    username = db.Column(db.String(100), primary_key=True)
    encpwd = db.Column(db.String(100))
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
