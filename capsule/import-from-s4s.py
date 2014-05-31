#!/usr/bin/env python

import ucsv, sys, argparse, requests, json, urllib
from datetime import datetime
from requests.auth import HTTPBasicAuth

CAPSULE_TOKEN = '02cba853e82ede5f2b99947b8a717b94'
CAPSULE_SITE = 'https://rethinkdb.capsulecrm.com'
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
total_rows = len(rows)

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

    # Create the new user on Capsule
    req = add_data('/api/person', person_data)
    person_id = req.headers['location'].rsplit('/',1)[1]

    # Add tags to the person we just created
    add_tag(person_id,UNREVIEWED_TAG)
    add_tag(person_id,SOURCE_TAG)

    # Note their shirt story in the history
    date = datetime.strptime(row['Date Created'], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%SZ")
    note = "Shirts for stories submission\n-----\n"+row['What are you using RethinkDB for?']
    history_data = {
        'historyItem': {
            'entryDate': date,
            'note': note
        }
    }
    req = add_data('/api/party/'+person_id+'/history', history_data)

    print "[%d/%d] Adding person: %s" % (i+1, total_rows, name)

