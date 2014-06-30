#!/usr/bin/env python

from flask import Flask, render_template, request
from flask.ext.socketio import SocketIO, emit
import rethinkdb as r
from threading import Thread
import random

app = Flask(__name__)
socketio = SocketIO(app)

conn = r.connect()
checkins = r.db('meetup').table('checkins').changes().run(conn)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@socketio.on('connect')
def print_checkin():
    print 'TESTING'
    emit('checkin', 'qweqw', broadcast=True)

#t = Thread(target=print_checkin) 
#t.start()
if __name__ == '__main__':
    socketio.run(app)
    print "hello"
