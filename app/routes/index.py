from app import app
from app import db
from app.models import Track
from flask import jsonify
import json

tracklist = Track.query.all()

print tracklist

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/admin')
def adminPage():
	return app.send_static_file('admin.html')

@app.route('/tracks.json')
def tracks():
    return jsonify(tracknames = [i.names for i in tracklist])
