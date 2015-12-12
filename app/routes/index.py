from app import app
from app import db
from app.models import Convention, Event, Track, Room, RoomGroup, Timeslot
from flask import jsonify
import json


@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/admin')
def adminPage():
    return app.send_static_file('/views/admin.html')

@app.route('/convention.json')
def convention():
    conventions = Convention.query.all()
    return jsonify(configs = [i.configs for i in conventions])

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
        'room': {'id':'room','name':'Room',},
        'type': {'id':'type','name':'Type',},
        'presenters': {'id':'presenters','name':'Program Participants',},
        'resources': {'id':'resources','name':'Resources',},
        'description': {'id':'description','name':'Description',},
        'comments': {'id':'comments','name':'Staff Comments',},
        })

@app.route('/eventlist.json')
def events():
    eventlist = Event.query.all()
    return jsonify(eventlist = [i.useroutput for i in eventlist])

@app.route('/rooms.json')
def rooms():
    roomlist = Room.query.all()
    return jsonify(
        rooms = [i.ui_rooms for i in roomlist]
        )

@app.route('/room_groups.json')
def room():
    roomgrouplist = RoomGroup.query.all()
    return jsonify(
        room_groups = [i.ui_room_groups for i in roomgrouplist],
        )

@app.route('/configs.json')
def combined_info():
    convention = Convention.query.first()
    number_of_timeslots = Timeslot.query.count()
    tracks = Track.query.all()
    rooms = Room.query.all()
    room_groups = RoomGroup.query.all()
    return jsonify(
        {
            "convention": {
                "name": convention.name,
                "start_dt": convention.start_dt.strftime(convention.datetime_format),
                "timeslot_length": int(convention.timeslot_duration.total_seconds()/60),
                "number_of_timeslots": number_of_timeslots
            },
            "tracks": [i.names for i in tracks],
            "rooms": [{"name": i.room_name,
                       "capacity": i.room_capacity,
                       "sq_ft": i.room_sq_ft,
                       "group_id": i.room_group_id,
                       "id": i.id,
                       "available_timeslots": [{"name": j.name,
                                                "index": j.timeslot_index
                                                }
                                               for j in i.available_timeslots],
                       "suitable_events": [{"id": j.id,
                                            "title": j.title
                                            }
                                           for j in i.suitable_events]
                       }
                      for i in rooms],
            "room_groups": [i.ui_room_groups for i in room_groups]
        }
    )
