#!/usr/bin/env python

import ucsv, sys, argparse, requests, json, urllib
from datetime import datetime
from requests.auth import HTTPBasicAuth
from multiprocessing import Pool
"""
CAPSULE_TOKEN = '02cba853e82ede5f2b99947b8a717b94'
CAPSULE_SITE = 'https://rethinkdb.capsulecrm.com'
"""
# Credentials for testing
CAPSULE_TOKEN = '96151e6b49271a39f2b139f23b02af32'
CAPSULE_SITE = 'https://rethinkdb-testing.capsulecrm.com'

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
def update_user(user_map):
    print "Updating user: "+user_map[1]
    data = {
        'customFields': {
            'customField': [
                {
                    'label': '__github',
                    'text': user_map[1],
                }
            ]
        }
    }
    return requests.post(CAPSULE_SITE+'/api/party/'+user_map[0]+'/customfields', data=json.dumps(data), auth=auth, headers=headers)

def start():
    parties = {}
    url = CAPSULE_SITE + '/api/party'
    req = requests.get(url, auth=auth, headers=headers)
    users = json.loads(req.text)['parties']['person']

    user_map = []
    for user in users:
        try:
            websites = user['contacts']['website']
            # If there's one website, it's a dict, otherwise, it's a list of dicts
            if len(websites) == 0:
                continue
            elif type(websites) is dict:
                websites = [websites]
            for service in websites:
                if service['webService'] == 'GITHUB':
                    user_map.append([user['id'],service['webAddress']])
        except KeyError:
            continue

    # Look up info on each user
    p = Pool(10)
    success = p.map(update_user, user_map)

if __name__ == "__main__":
    start()
