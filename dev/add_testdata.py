"""
Inserts test data into the CREM database.
"""

import sys
import os
import csv
import random
random.seed()

script_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(script_dir, '..')))

from app import db
from app.models import Track, Event, Resource, Presenter, Room, RoomGroup

# Delete records from tables of interest.
Track.query.delete()
Event.query.delete()
Resource.query.delete()
Presenter.query.delete()
Room.query.delete()
RoomGroup.query.delete()

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

for track_info in track_infos:
    track = Track(track_info[0], track_info[1])
    db.session.add(track)

# Commit the test data to the database.
db.session.commit()

# Add events.

# The track name in TuxTrax and the corresponding name in CREM.
tuxtrax_tracks = {
    'literature': 'Literature',
    'tech': 'Tech',
    'after-dark': 'After Dark',
    'action-adventure': 'Action Adventure',
    'costuming': 'Costuming',
    'webcomics': 'Web Comics',
    'gaming': 'Gaming',
    'diy': 'D.I.Y.',
    'film': 'Film',
    'food': 'Food',
    'video-gaming': 'Video Gaming',
    'science': 'Science',
    'eco': 'Eco',
}

# Read events from events file.
events_file = open(os.path.join(script_dir, 'test_events.txt'), 'rb')
csvreader = csv.reader(events_file, delimiter='|', quotechar='"')
first_row = True
for row in csvreader:
    if first_row:
        # Skip the header line.
        first_row = False
        continue
    if row[2] in tuxtrax_tracks:
        track_name = tuxtrax_tracks[row[2]]
    else:
        # There is no corresponding track in CREM at this time.
        continue
    event = Event()
    event.title = row[0]
    event.description = unicode(row[1], 'utf8')
    event.track = db.session.query(Track).\
        filter(Track.name == track_name).first()
    event.duration = int(row[3])
    event.failityRequest = row[4]
    db.session.add(event)
events_file.close()

# Commit the test data to the database.
db.session.commit()

# Add resources.

# For each Resource, the name, request form label and whether
# the resource should be displayed.
resource_infos = (
    ('Projector', 'This event CANNOT happen without a projector', True),
    ('Microphone/sound system',
     'This event CANNOT happen without a microphone and sound system', True),
    ('Drinking water', 'Drinking water', True),
    ('Quiet (no airwalls)', 'Quiet (no airwalls)', True),
)

for resource_info in resource_infos:
    resource = Resource(resource_info[0], resource_info[1], resource_info[2])
    db.session.add(resource)

# Commit the test data to the database.
db.session.commit()

# Add presenters.

# For each presenter, their first name, last name, email address and
# phone number.
presenter_infos = (
    ('Matt', 'Arnold', 'matt.mattarn@gmail.com', ''),
    ('Kell', 'Carnahan', 'wyndsung@gmail.com', '612-720-5144'),
    ('Jessica', 'Roland', 'theroland4@gmail.com', ''),
    ('William', 'Pribble', 'wmpribble@gmail.com', '616-808-6123'),
    ('Joe', 'Rapp', 'joerapp14@gmail.com', '586-894-3911'),
    ('Melanie', 'Castle', 'disjointedimages@gmail.com', ''),
    ('Dan', 'Johns', 'danjohns7@gmail.com', ''),
    ('Dawn', 'Marino', 'mrsbruhaha@gmail.com', ''),
    ('Sarah', 'Elkins', 'sarah.elkins@gmail.com', '301-613-4393'),
    ('Jen', 'Talley', 'mimiboo9@gmail.com', '7347319771'),
    ('cassinator', '', 'cassinator09@gmail.com', ''),
    ('mwlauthor', '', '', ''),
    ('Leah', 'Rapp', 'leah.rapp@gmail.com', ''),
    ('Bob', 'Trembley', 'balroggamer@gmail.com', ''),
    ('Kent', 'Newland', 'kentbobii@gmail.com', ''),
    ('Angela', 'Rush', 'angierae@gmail.com', '248-505-1551'),
    ('Brittany', 'Burke', 'brittany.burke@gmail.com', '248-259-5122'),
    ('Stu', 'Chisholm', 'djstucrew@gmail.com', '(586) 773-6182'),
    ('Joshua', 'DeBonis', 'josh@sortasoft.com', '203.470.7264'),
    ('Nikita', 'Mikros', 'nik@smashworx.com', ''),
)

for presenter_info in presenter_infos:
    presenter = Presenter(presenter_info[0], presenter_info[1])
    presenter.email = presenter_info[2]
    presenter.phone = presenter_info[3]
    db.session.add(presenter)

# Commit the test data to the database.
db.session.commit()

# Assign a random set of presenters to each event.
events = Event.query.all()
presenters = Presenter.query.all()
for event in events:
    # Randomly select from 0 to 4 presenters for this event.
    random_presenters = random.sample(presenters, random.randrange(5))
    event.presenters = random_presenters

# Commit the test data to the database.
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

# Commit the test data to the database.
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

for room_info in room_infos:
    room = Room()
    room.room_name = room_info[0]
    room.room_sq_ft = room_info[1]
    room.room_capacity = room_info[2]
    if room_info[3]:
        room.room_group = db.session.query(RoomGroup).\
            filter(RoomGroup.room_group_name == room_info[3]).first()
    db.session.add(room)

# Commit the test data to the database.
db.session.commit()
