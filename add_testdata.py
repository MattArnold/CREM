"""
Inserts test data into the CREM database.
"""

from app import db
from app.models import Track

# Delete all exsiting tracks.
tracks = Track.query.all()
for tracks in tracks:
    db.session.delete(tracks)
db.session.commit()

# Add tracks.

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
