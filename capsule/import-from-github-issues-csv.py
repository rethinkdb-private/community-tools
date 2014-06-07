#!/usr/bin/env python

import ucsv, sys, argparse, requests, json, urllib
from datetime import datetime
from requests.auth import HTTPBasicAuth
from multiprocessing import Pool
import copy

GITHUB_TOKEN = '3df11993e5fa5e4b0c661b7abc965345f028c04d'
"""
CAPSULE_TOKEN = '02cba853e82ede5f2b99947b8a717b94'
CAPSULE_SITE = 'https://rethinkdb.capsulecrm.com'
"""
# Credentials for testing
CAPSULE_TOKEN = '96151e6b49271a39f2b139f23b02af32'
CAPSULE_SITE = 'https://rethinkdb-testing.capsulecrm.com'

IMPORTED_TAG = 'Imported'
UNREVIEWED_TAG = 'Unreviewed'
SOURCE_TAG = 'GitHub issues'
auth = HTTPBasicAuth(CAPSULE_TOKEN, 'x')
headers={
    'Accept': 'application/json',
    'content-type': 'application/json'    
}
gh_headers={
    'Authorization': 'token ' + GITHUB_TOKEN,
}

# Utility functions to modify and access dicts using a path
def get_nested(d, path):
    keys = path.split('.')
    branch = d
    for key in keys:
        if type(branch) is not dict:
            return None
        branch = branch.get(key, {})
    return branch

def set_nested(d, path, value):
    keys = path.split('.')
    branch = d
    for key in keys[:-1]:
        # If we haven't finished expanding the path, but find an object that
        # isn't a dict along the way, just return early.
        if type(branch) is not dict:
            return 
        branch = branch.setdefault(key, {})
    if type(branch) is dict:
        branch[keys[-1]] = value

# Utility methods for posting resources and tags to Capsule
def add_data(resource, data):
    req = requests.post(CAPSULE_SITE+resource, data=json.dumps(data), auth=auth, headers=headers)
    if not req.status_code in [200, 201]:
        print "HTTP %d when adding Capsule data for resource %s\nData:%s\nResponse:%s" % (req.status_code, resource, json.dumps(data), req.text)
        return None
    return req
def add_tag(party_id, tag, name):
    req = requests.post(CAPSULE_SITE+'/api/party/'+party_id+'/tag/'+urllib.quote_plus(tag), auth=auth)
    if not req.status_code in [200, 201]:
        print 'Error adding tag %s to %s: %s' % (tag, name, req.text)
        return None
    return req
def get_matching_user(github_login):
    req = requests.get(CAPSULE_SITE+'/api/party?q='+github_login, auth=auth, headers=headers)
    if req.status_code is not 200:
        print "HTTP %d when looking up user details on Capsule for %s" % (req.status_code, github_login)

    matching = json.loads(req.text)
    if matching['parties']['@size'] == '0':
        return None

    # Look at the parties we get back from Capsule -- we're only looking at those that are "person"
    for party_type, party in matching['parties'].iteritems():
        if party_type == 'person':
            # For each person that is returned, make sure they've got at least
            # one contact, and then look up their GitHub id to make sure they match
            if type(party) is dict:
                party = [party] # make sure we have a list if the API returns a dict for a single user
            for user in party:
                if type(user['contacts']) is dict:
                    try:
                        websites = user['contacts']['website']
                        # If there's one website, it's a dict, otherwise, it's a list of dicts
                        if len(websites) == 0:
                            continue
                        elif type(websites) is dict:
                            websites =[websites]
                        for service in websites:
                            # Matched a GitHub id, return the user
                            if service['webService'] == 'GITHUB' and service['webAddress'] == github_login:
                                return { 'person': user }
                    except KeyError:
                        continue
    return None
def update_user(user_id, user_data, name):
    url = CAPSULE_SITE+'/api/person/'+user_id
    req = requests.put(url, data = json.dumps(user_data), auth=auth, headers=headers)
    if req.status_code is not 200:
        print "HTTP %d when updating Capsule user %s (%s): %s : %s" % (req.status_code, user_id, name, url, req.text)
        print "Capsule rejects invalid email addresses. Email for %s: %s" % (name, get_nested(user_data, 'person.contacts.email.emailAddress'))
    return req

def add_user_to_capsule(user):
    gh_user = user['info']
    events = user['events']
    name = "%s %s" % (gh_user['first_name'], gh_user['last_name'])

    # New data we fetched from GitHub on the user (derived from the CSV)
    new_user = {
        'person': {
            'firstName': gh_user['first_name'],
            'lastName': gh_user['last_name'],
            'contacts': {
                'website': [
                    {
                        'webService': 'GITHUB',
                        'webAddress': gh_user['login'],
                    }
                ],
            },
        }
    }

    if not gh_user['first_name'] and not gh_user['last_name']:
        new_user['person']['firstName'] = gh_user['login']

    # If we have any of these attributes in the GitHub details, add them to our new user data
    for attrs in [('bio', 'about'), ('company', 'organisationName')]:
        attr = attrs[0]
        new_attr = attrs[1]
        if gh_user[attr]:
            new_user['person'][new_attr] = gh_user[attr]
    if gh_user['email']:
        set_nested(new_user, 'person.contacts.email.emailAddress', gh_user['email'])
    if gh_user['location']:
        set_nested(new_user, 'person.contacts.address.city', gh_user['location'])
    if gh_user['blog']:
        new_user['person']['contacts']['website'].append({
            'webService': 'URL',
            'webAddress': gh_user['blog']
        })

    # Get the user from Capsule, if they exist
    existing_user = get_matching_user(gh_user['login']) 

    # The user doesn't exist, so add the user to Capsule
    if existing_user is None:
        print "Adding user %s that doesn't exist in Capsule" % gh_user['login']
        # Create the new user on Capsule
        req = add_data('/api/person', new_user)
        if req and req.headers:
            person_id = req.headers['location'].rsplit('/',1)[1]
        else:
            print "Skipping user %s because of an error." % gh_user['login']
            return
    # The user exists, so resolve conflicts and update the user in Capsule
    else:
        merged_user = merge_user(existing_user, new_user)
        # Get the person's id
        person_id = existing_user['person']['id']
        if len(merged_user['person']) > 0:
            print "Merged user %s and adding to Capsule" % gh_user['login']
            req = update_user(person_id, merged_user, name)
            if not req:
                return

    # Add tags to the person we just created
    for tag in [UNREVIEWED_TAG, IMPORTED_TAG, SOURCE_TAG]:
        req = add_tag(person_id, tag, name)

    # Note the events for the user, but only if this is a new user
    for event in events:
        print "Adding event by %s: %s on %s" % (gh_user['login'], event['event'], event['timestamp'])
        if event['event'] == 'opened_issue':
            note = "Opened "
        elif event['event'] == 'added_comment':
            note = "Added comment to "
        note += "issue #%s: %s\nPermalink: %s\n-----\n%s" % (event['issue'], event['issue_title'], event['permalink'], event['body'])

        history_data = {
            'historyItem': {
                'entryDate': event['timestamp'],
                'note': note
            }
        }
        req = add_data('/api/party/'+person_id+'/history', history_data)

# Merge an existing Capsule user with new user data from GitHub
def merge_user(existing_user, new_user):
    if not existing_user.get('person') or not new_user.get('person'):
        print "New or existing user is missing a top-level 'person' field:\n\nExisting user: %s\n\nNew user: %s" % (existing_user, new_user)
        return

    # Dive into the top-level 'person' attribute to make it easier to address the dicts
    existing_user = existing_user['person']
    new_user = new_user['person']

    # Clone the existing user as a nested dict
    merged_user = {}

    # Fill in missing fields
    fields = [
        'firstName',
        'lastName',
        'about',
        'organisationName',
        'contacts.email.emailAddress',
        'contacts.address.city',
    ]
    # For each attribute path, if we have data on a new user that's not in the
    # existing user profile, add it as part of the merge.
    for attr in fields:
        if get_nested(new_user, attr) and not get_nested(existing_user, attr):
            set_nested(merged_user, attr, get_nested(new_user, attr))

    # Note: Since we found this person by looking up their GitHub profile, they
    # already have one web service guaranteed (for GitHub).  We also don't need
    # to merge a GitHub id into their list of web services, only their blog (if
    # they have one).

    # Add a blog if it doesn't exist.
    def find_blog(user):
        websites = get_nested(user, 'contacts.website')
        # If there's one website, it's a dict, otherwise, it's a list of dicts,
        # so make sure we have a list.
        if type(websites) is dict:
            websites = [websites]
        for website in websites:
            if website['webService'] == 'URL':
                return website
        return None
    
    new_user_blog = find_blog(new_user)
    if new_user_blog:
        # If we don't already have a website of the type URL (e.g. a blog), merge it into the profile
        if not find_blog(existing_user):
            # Get the existing set of websites for this user
            existing_websites = get_nested(existing_user, 'contacts.website')
            # If there's just one web service (e.g. just their GitHub profile), there will be a dict -- we need to make sure it's a list.
            if type(existing_websites) is dict:
                existing_websites = [existing_websites]
            merged_websites = existing_websites.append(new_user_blog)
            set_nested(merged_user, 'contacts.website', merged_websites)

    return {'person': merged_user }


def start_import():
    # Command-line argument: specify the CSV data file
    parser = argparse.ArgumentParser(description='Imports a GitHub issues CSV into Capsule.')
    parser.add_argument('issues_csv', help='the GitHub issues CSV data file to import')
    parser.add_argument('users_csv', help='the GitHub users CSV data file to import')
    args = parser.parse_args()

    def read_csv(csv):
        try:
            reader = ucsv.UnicodeDictReader(open(csv))
        except IOError:
            print "Could not read the specified CSV data file: %S" % args.issues_csv
            sys.exit()
        return list(reader)

    issues = read_csv(args.issues_csv)
    gh_users = read_csv(args.users_csv)

    # Reorganize the data as a set of events per user
    users = {}
    for row in issues:
        event =  {
            'timestamp': row['timestamp'],
            'event': row['event'],
            'permalink': row['permalink'],
            'issue': row['issue'],
            'issue_title': row['issue_title'],
            'body': row['body']
        }
        user = row['user']
        if user not in users:
            users[user] = {
                'info': {},
                'events': []
            }

        users[user]['events'].append(event)

    # Add GitHub info on each user to our data set
    for row in gh_users:
        users[row['login']]['info'] = row

    # Sort events of each user by date, then add them to Capsule
    for user in users:
        users[user]['events'].sort(key=lambda x: x['timestamp'])

    # Add users using a multiprocessing pool
    print "Adding %d users to Capsule." % len(users)
    p = Pool(10)
    p.map(add_user_to_capsule, users.values())

if __name__ == "__main__":
    start_import()
