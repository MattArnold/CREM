"""
Inserts test data into the CREM database.
"""

import sys
import os
import csv

script_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(script_dir, '..')))

from app import db
from app.models import Track, Event, Resource, Presenter

# Delete all exsiting tracks.
tracks = Track.query.all()
for track in tracks:
    db.session.delete(track)
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

for track_info in track_infos:
    track = Track(track_info[0], track_info[1])
    db.session.add(track)

# Commit the test data to the database.
db.session.commit()

# Delete all exsiting events.
events = Event.query.all()
for event in events:
    db.session.delete(event)
db.session.commit()

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

# Delete all exsiting resources.
resources = Resource.query.all()
for resource in resources:
    db.session.delete(resource)
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
