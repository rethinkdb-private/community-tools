#!/usr/bin/env python
"""
Usage:
    seed-data.py fetch
    seed-data.py update
"""

import requests, json, argparse, pprint, random, time, names, uuid, copy
from datetime import datetime
from docopt import docopt
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

def fetch_meetup_data():
    # Meetup needs ms since epoch when specifying a date range
    from_date = int(meetup_api['date'].epoch() * 1000)
    to_date = int(meetup_api['date'].next_day(1).epoch() * 1000)
    url = "https://api.meetup.com/2/open_events.json?category=%s&zip=%s&time=%d,%d&key=%s" % (meetup_api['category'], meetup_api['zip'], from_date, to_date, meetup_api['token'])
    req = requests.get(url)
    results = req.json()
    meetups = map(lambda m: {
        'event_name': m['name'],
        'checkins': m['yes_rsvp_count'],
        'lat': m['venue']['lat'],
        'lon': m['venue']['lon'],
    }, results['results'])

    with open(meetup_api['file'], 'w') as f:
        json.dump(meetups, f)

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

    c = r.connect(rdb['host'],rdb['port'])
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

    print "%d checkins added to RethinkDB." % len(checkins)

def start():
    args = docopt(__doc__)
    if args['fetch']:
        fetch_meetup_data()
    elif args['update']:
        update_meetup_data()

if __name__ == "__main__":
    start()
