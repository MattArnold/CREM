from app import app
from app import db
from app.models import Event, Track
from flask import jsonify
import json


@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/admin')
def adminPage():
    return app.send_static_file('admin.html')

@app.route('/tracks.json')
def tracks():
    tracklist = Track.query.all()
    return jsonify(tracknames = [i.names for i in tracklist])

@app.route('/columns.json')
def columns():
    return jsonify(columnnames = [{'id':'eventnumber','name':'#',},{'id':'title','name':'Title',},{'id':'track','name':'Track',},{'id':'start','name':'Start',},{'id':'duration','name':'Duration',},{'id':'room','name':'Room',},{'id':'type','name':'Type',},{'id':'presenters','name':'Program Participants',},{'id':'description','name':'Description',}])

@app.route('/eventlist.json')
def events():
    eventlist = Event.query.all()
    return jsonify(eventlist = [i.useroutput for i in eventlist])