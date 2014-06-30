#!/usr/bin/env python
import requests, json, argparse, pprint, random, time, names, uuid, copy
from flask import Flask
from datetime import datetime
from delorean import Delorean
import rethinkdb as r

rdb = {
    'host': 'localhost',
    'port': 28015,
    'db': 'meetup',
    'table': 'checkins',
}
meetup_api = {
    'token': '2c702f2c5158106c34637a5a4cb2a1f',
    'category': '34', # Tech category
    'city': 'San Francisco',
    'zip': '94101',
    'file': 'meetups.json',
    'date': Delorean(datetime=datetime(2014,7,1,0,0,0,0), timezone="US/Pacific"),
}

app = Flask(__name__)

@app.route('/fetch')
def fetch_meetup_data():
    # Meetup needs ms since epoch when specifying a date range
    from_date = int(meetup_api['date'].epoch() * 1000)
    to_date = int(meetup_api['date'].next_day(1).epoch() * 1000)
    url = "https://api.meetup.com/2/open_events.json?category=%s&zip=%s&time=%d,%d&key=%s" % (meetup_api['category'], meetup_api['zip'], from_date, to_date, meetup_api['token'])
    req = requests.get(url)
    results = req.json()
    meetups = []
    for m in results['results']:
        # Skip meetups that don't have a venue       
        if 'venue' not in m:
            continue
        meetups.append({
            'event_name': m['name'],
            'checkins': m['yes_rsvp_count'],
            'lat': m['venue']['lat'],
            'lon': m['venue']['lon'],
        })

    with open(meetup_api['file'], 'w') as f:
        json.dump(meetups, f)

    return "Fetched data from Meetup."

@app.route('/update')
def update_meetup_data():
    with open(meetup_api['file'],'r') as f:
        meetups = json.load(f)

    checkins = []
    for meetup in meetups:
        # drop the RethinkDB event
        if 'rethinkdb' not in meetup['event_name'].lower():
            for x in range(meetup['checkins']):
                meetup = copy.deepcopy(meetup)
                meetup.update({
                    'first_name': names.get_first_name(),
                    'last_name': names.get_last_name(),
                    #'id': str(uuid.uuid4())
                })
                checkins.append(meetup)
    random.shuffle(checkins)

    try:
        c = r.connect(rdb['host'],rdb['port'])
    except r.RqlDriverError as e:
        return "RethinkDB error: "+str(e)
    if rdb['db'] not in r.db_list().run(c):
        r.db_create(rdb['db']).run(c)
    if rdb['table'] not in r.db(rdb['db']).table_list().run(c):
        r.db(rdb['db']).table_create(rdb['table']).run(c)

    table = r.db(rdb['db']).table(rdb['table'])
    table.delete().run(c)

    for checkin in checkins:
        table.insert(checkin).run(c)
        #time.sleep(1)
        #time.sleep(1.0/random.randint(1,50))

    return "%d checkins added to RethinkDB." % len(checkins)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
