#!/usr/bin/env python

import ucsv, sys, argparse, requests, json, urllib
from datetime import datetime
from requests.auth import HTTPBasicAuth
from multiprocessing import Pool
CAPSULE_TOKEN = '02cba853e82ede5f2b99947b8a717b94'
CAPSULE_SITE = 'https://rethinkdb.capsulecrm.com'
"""
# Credentials for testing
CAPSULE_TOKEN = '96151e6b49271a39f2b139f23b02af32'
CAPSULE_SITE = 'https://rethinkdb-testing.capsulecrm.com'
"""

IMPORTED_TAG = 'Imported'
UNREVIEWED_TAG = 'Unreviewed'
SOURCE_TAG = 'Shirts for stories'
auth = HTTPBasicAuth(CAPSULE_TOKEN, 'x')
headers={
    'Accept': 'application/json',
    'content-type': 'application/json'    
}

# Utility methods for posting resources and tags to Capsule
def add_data(resource, data):
    return requests.post(CAPSULE_SITE+resource, data=json.dumps(data), auth=auth, headers=headers)
def add_tag(party_id, tag):
    return requests.post(CAPSULE_SITE+'/api/party/'+party_id+'/tag/'+urllib.quote_plus(tag), auth=auth)

def add_user(data):
    user = data['user']
    timestamp = data['timestamp']
    story = data['story']

    name = user['person']['firstName'] + ' ' + user['person']['lastName']
    # Create the new user on Capsule
    req = add_data('/api/person', user)
    person_id = req.headers['location'].rsplit('/',1)[1]

    # Add tags to the person we just created
    for tag in [UNREVIEWED_TAG, IMPORTED_TAG, SOURCE_TAG]:
        req = add_tag(person_id, tag)
        if not req.status_code is 201:
            print 'Error adding tag %s to %s: %s' % (tag, name, req.text)

    # Note their shirt story in the history
    date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%SZ")
    note = "Shirts for stories submission\n-----\n"+story
    history_data = {
        'historyItem': {
            'entryDate': date,
            'note': note
        }
    }
    req = add_data('/api/party/'+person_id+'/history', history_data)

    print "Adding person: %s" % name
    

def start():
    # Command-line argument: specify the CSV data file
    parser = argparse.ArgumentParser(description='Imports a Wufoo CSV into Capsule.')
    parser.add_argument('csv', help='the Wufoo CSV data file to import')
    args = parser.parse_args()

    try:
        reader = ucsv.UnicodeDictReader(open(args.csv))
    except IOError:
        print "Could not read the specified CSV data file: %S" % args.csv
        sys.exit()

    rows = list(reader)
    users = []

    for i, row, in enumerate(rows):
        # Name of the user
        name = row['Name']
        split_name = name.rsplit(' ',1)
        first_name = split_name[0]
        if len(split_name) > 1:
            last_name = split_name[1]
        else:
            last_name = ''

        # Put together data on the user
        person_data = {
            'person': {
                'firstName': first_name,
                'lastName': last_name,
                'contacts': {
                    'email': {
                        'emailAddress': row['Email address'],
                    },
                }
            }
        }

        # If we have a GitHub username, add it to their contact details
        if row['Github username']:
            person_data['person']['contacts']['website'] = {
                'webService': 'GITHUB',
                'webAddress': row['Github username'],
            }

        users.append({
            'user': person_data,
            'timestamp': row['Date Created'],
            'story': row['What are you using RethinkDB for?'],
        })

    # Add users using a multiprocessing pool
    print "Adding %d users to Capsule." % len(rows)
    p = Pool(10)
    p.map(add_user, users)

if __name__ == "__main__":
    start()
