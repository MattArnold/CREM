"""
Inserts data into the CREM database.
"""

import sys
import os
import unicodecsv as csv
import datetime

script_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(script_dir, '..')))

CONVENTION_INFO_FNAME = 'convention_info.csv'


def get_timeslots(start_date_str, start_time_str, duration_str,
                  convention, Timeslot):
    """
    Given a start date and time and end date and time for an event, return a
    list of timeslots. Dates have the format "mm/dd/yyyy" and times have the
    format "hh:mm" in 24-hour time.
    """
    # The list of timeslots to return.
    timeslots = []

    # Create datetime object for the start and end of the event.
    event_start_dt = datetime.datetime.strptime('%s %s' % (start_date_str, start_time_str),
                                                '%m/%d/%Y %H:%M')

    # Calculate the length of each timeslot in seconds.
    num_timeslot_seconds = convention.timeslot_duration.total_seconds()

    # Calculation the number of timeslots for this event.
    if not duration_str.strip():
        num_timeslots = 1
    else:
        num_hours = int(duration_str.split(':')[0].replace('hr', ''))
        num_minutes = int(duration_str.split(':')[1].replace('min', ''))
        num_event_seconds = (num_hours * 60 + num_minutes) * 60
        num_timeslots = num_event_seconds//num_timeslot_seconds + 1

    # Determine the index of the first timeslot of the event.
    num_seconds_since_conv_start = (event_start_dt - convention.start_dt).total_seconds()
    if num_seconds_since_conv_start < 0:
        raise Exception('Error: event occurs before start of convention')
    first_index = num_seconds_since_conv_start/num_timeslot_seconds

    # Add timeslots to the list.
    timeslot_indexes = range(int(first_index), int(first_index) + int(num_timeslots))
    for timeslot_index in timeslot_indexes:
        timeslot = Timeslot.query.filter_by(timeslot_index=timeslot_index).first()
        timeslots.append(timeslot)

    return timeslots


def refresh_data(sched_info_fname, convention_info_fname=CONVENTION_INFO_FNAME):
    from app import db
    from app.models import Convention, Timeslot, Track, Event, Presenter
    from app.models import Room, RoomGroup, DataLoadError

    # Delete records from tables of interest.
    DataLoadError.query.delete()
    Convention.query.delete()
    Timeslot.query.delete()
    Track.query.delete()
    Event.query.delete()
    Presenter.query.delete()
    Room.query.delete()
    RoomGroup.query.delete()

    # Define the convention.

    convention = Convention()
    with open(CONVENTION_INFO_FNAME, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        first_row = True
        for row in csvreader:
            if first_row:
                first_row = False
            else:
                convention.name = row[0]
                convention.description = row[1]
                convention.date_format = row[5]
                convention.datetime_format = row[6]
                convention.start_dt = datetime.datetime.strptime(row[2], convention.datetime_format)
                convention.end_dt = datetime.datetime.strptime(row[3], convention.datetime_format)
                convention.timeslot_duration = datetime.timedelta(0, int(row[4])*60) # Minutes converted to seconds.
                convention.url = row[7]
                convention.active = True

                # There is only one row of convention data.
                break
    db.session.add(convention)
    db.session.commit()

    # Commit the data to the database.
    db.session.commit()

    # Create timeslots.
    timeslot_count = int((convention.end_dt - convention.start_dt).total_seconds() /
                         convention.timeslot_duration.total_seconds())
    for n in range(timeslot_count):
        timeslot = Timeslot(n)
        timeslot.active = True
        db.session.add(timeslot)

    # Commit the data to the database.
    db.session.commit()

    # Add tracks.

    # The track name and the email address for each CREM track.
    track_infos = (
        ('Literature', 'literature@penguicon.org'),
        ('Tech', 'tech@penguicon.org'),
        ('After Dark', 'afterdark@penguicon.org'),
        ('Action Adventure', 'action@penguicon.org'),
        ('Costuming', 'costuming@penguicon.org'),
        ('Web Comics', 'webcomics@penguicon.org'),
        ('Gaming', 'gaming@penguicon.org'),
        ('D.I.Y.', 'diy@penguicon.org'),
        ('Film', 'film@penguicon.org'),
        ('Food', 'food@penguicon.org'),
        ('Video Gaming', 'videogaming@penguicon.org'),
        ('Science', 'science@penguicon.org'),
        ('Eco', 'eco@penguicon.org'),
    )

    # Create tracks and save database objects in dictionary for later reference.
    tracks = {}
    for track_info in track_infos:
        track = Track(track_info[0], track_info[1])
        tracks[track_info[0]] = track
        db.session.add(track)

    # Commit the data to the database.
    db.session.commit()

    # Add room groups.

    room_group_names = (
        'Algonquin',
        'Charlevoix',
        'Lobby',
    )

    for room_group_name in room_group_names:
        room_group = RoomGroup(room_group_name)
        db.session.add(room_group)

    # Commit the data to the database.
    db.session.commit()

    # Add rooms.

    # For each room, the name, square feet, capacity and room group it belongs to.
    room_infos = (
        ('Algonquin A', 1207, 100, 'Algonquin'),
        ('Algonquin B', 1207, 100, 'Algonquin'),
        ('Algonquin C', 1207, 100, 'Algonquin'),
        ('Algonquin D', 1207, 100, 'Algonquin'),
        ('Algonquin Foyer', 3000, 450, None),
        ('Charlevoix A', 756, 64, 'Charlevoix'),
        ('Charlevoix B', 756, 64, 'Charlevoix'),
        ('Charlevoix C', 756, 64, 'Charlevoix'),
        ('Portage Auditorium', 1439, 68, None),
        ('Windover', 1475, 40, None),
        ('TC Linguinis', 1930, 40, None),
        ('Baldwin Board Room', 431, 12, None),
        ('Board of Directors', 511, 15, None),
        ('Board of Governors', 391, 5, None),
        ('Board of Regents', 439, 15, None),
        ('Board of Trustees', 534, 40, None),
        ('Hamlin', 360, 25, None),
        ('Montcalm', 665, 50, None),
        ('Nicolet', 667, 50, None),
        ('Game Table A', 20, 10, 'Lobby'),
        ('Game Table B', 20, 10, 'Lobby'),
        ('Game Table C', 20, 10, 'Lobby'),
        ('Game Table D', 20, 10, 'Lobby'),
    )

    # Create rooms and save database objects in dictionary for later reference.
    rooms = {}
    for room_info in room_infos:
        room = Room()
        room.room_name = room_info[0]
        room.room_sq_ft = room_info[1]
        room.room_capacity = room_info[2]
        if room_info[3]:
            room.room_group = db.session.query(RoomGroup).\
                filter(RoomGroup.room_group_name == room_info[3]).first()
        rooms[room.room_name] = room
        db.session.add(room)

    # Commit the data to the database.
    db.session.commit()

    # Keep track of presenters.
    presenters = {}

    # Read events from file.
    with open(sched_info_fname, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        first_row = True
        for row in csvreader:
            if first_row:
                first_row = False
                continue
            else:
                if row[5] not in tracks:
                    # There is no corresponding track in CREM at this time.
                    load_error = DataLoadError()
                    load_error.error_level = 'Error'
                    load_error.destination_table = 'event'
                    load_error.line_num = csvreader.line_num
                    load_error.error_msg = '%s is not a defined track; skipping this event' % row[5]
                    load_error.error_dt = datetime.datetime.now()
                    db.session.add(load_error)
                    continue
                event = Event()
                event.title = row[6]
                event.description = row[8]
                event.track = tracks[row[5]]

                # Add timeslots and duration.
                try:
                    timeslots = get_timeslots(row[0], row[1], row[9],
                                              convention, Timeslot)
                except Exception, e:
                    load_error = DataLoadError()
                    load_error.error_level = 'Error'
                    load_error.destination_table = 'event'
                    load_error.line_num = csvreader.line_num
                    load_error.error_msg = str(e)
                    load_error.error_dt = datetime.datetime.now()
                    db.session.add(load_error)
                    continue

                event.timeslots = timeslots
                event.duration = len(timeslots)

                event.failityRequest = row[10]
                event.convention = convention

                # Add room to the event.
                if row[4] not in rooms:
                    # This is not a predefined room, so add it.
                    load_error = DataLoadError()
                    load_error.error_level = 'Warning'
                    load_error.destination_table = 'event'
                    load_error.line_num = csvreader.line_num
                    load_error.error_msg = '%s is not a pre-defined room; adding this room' % row[4]
                    load_error.error_dt = datetime.datetime.now()
                    db.session.add(load_error)

                    room = Room()
                    room.room_name = row[4]
                    room.room_sq_ft = 0
                    room.room_capacity = 0
                    rooms[row[4]] = room
                    db.session.add(room)
                else:
                    room = rooms[row[4]]

                event.rooms = [room]

                # Add presenters.
                if row[7].strip():
                    presenter_names = row[7].split(',')
                    presenter_names = map(lambda s: s.strip(), presenter_names)
                    for presenter_name in presenter_names:
                        if presenter_name in presenters:
                            presenter = presenters[presenter_name]
                        else:
                            last_name = presenter_name.split(' ')[-1].strip()
                            first_name = ' '.join(presenter_name.split(' ')[0:-1]).strip()
                            presenter = Presenter(first_name, last_name)
                            presenters[presenter_name] = presenter
                            db.session.add(presenter)
                        event.presenters.append(presenter)

                db.session.add(event)

    # Commit the data to the database.
    db.session.commit()

if __name__ == '__main__':
    """
    Allows the data to be loaded from the command line, by passing the
    file name(s) as command line arguments.
    """
    script_dir = os.path.dirname(__file__)
    sys.path.append(os.path.abspath(os.path.join(script_dir, '..')))

    # Get the name of the files with schedule and convention information.
    if len(sys.argv) < 2:
        sys.stderr.write('Error: schedule information file not specified\n')
        sys.exit(1)
    sched_info_fname = sys.argv[1]

    # Make sure the file with schedule information exists.
    if not os.path.exists(sched_info_fname):
        sys.stderr.write('Error: %s does not exist\n' % sched_info_fname)
        sys.exit(1)

    # Get the name of file with convention information if specified.
    if len(sys.argv) > 2:
        convention_info_fname = sys.argv[2]
        if not os.path.exists(convention_info_fname):
            sys.stderr.write('Error: %s does not exist\n' % convention_info_fname)
            sys.exit(1)

    # Replace the data in the database.
    replace_data(sched_info_fname, convention_info_fname=CONVENTION_INFO_FNAME)
