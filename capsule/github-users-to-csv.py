#!/usr/bin/env python

import ucsv, sys, argparse, requests, json, urllib
from datetime import datetime
from multiprocessing import Pool
import copy

GITHUB_TOKEN = '3df11993e5fa5e4b0c661b7abc965345f028c04d'
headers={ 'Authorization': 'token ' + GITHUB_TOKEN, }

# Utility method: split name into first / last
def split_name(name):
    split_name = name.rsplit(' ',1)
    first_name = split_name[0]
    if len(split_name) > 1:
        last_name = split_name[1]
    else:
        last_name = ''
    return {
        'first_name': first_name,
        'last_name': last_name
    }

def get_user(login):
    req = requests.get("https://api.github.com/users/%s" % login, headers=headers)
    if req.status_code is not 200:
        print "HTTP %d when looking up user details for %s" % (req.status_code, login)
    user = json.loads(req.text)
    if 'name' in user and user['name'] is not None:
        name = split_name(user['name'])
    else:
        name = {
            'first_name': user['login'],
            'last_name': ''
        }

    user.setdefault('company','')
    user.setdefault('location','')
    user.setdefault('email','')
    user.setdefault('blog', '')
    user.setdefault('bio', '')
    
    print "Fetching data for %s (%s)" % (name['first_name'] + ' ' + name['last_name'], login)

    return {
        'first_name': name['first_name'],
        'last_name': name['last_name'],
        'login': user['login'],
        'followers': user['followers'],
        'company': user['company'],
        'location': user['location'],
        'email': user['email'],
        'blog': user['blog'],
        'bio': user['bio'],
    }

def start():
    # Command-line argument: specify the CSV data file
    parser = argparse.ArgumentParser(description='Outputs a CSV with info on users based on a GitHub issue data.')
    parser.add_argument('issues_csv', help='the input GitHub issues CSV data file')
    parser.add_argument('users_csv', help='the output CSV file with user data from GitHub')
    args = parser.parse_args()

    try:
        reader = ucsv.UnicodeDictReader(open(args.issues_csv))
    except IOError:
        print "Could not read the specified CSV data file: %S" % args.issues_csv
        sys.exit()
    issues = list(reader)

    # Reorganize the data as a set of events per user
    users = map(lambda x: x['user'], issues)
    users = list(set(users))

    # Add users using a multiprocessing pool
    print "Looking up %d users on GitHub." % len(users)
    p = Pool(10)
    users_with_data = p.map(get_user, users)

    with open(args.users_csv, 'wb') as f:
        writer = ucsv.UnicodeWriter(f)
        keys = [
            'first_name',
            'last_name',
            'login',
            'followers',
            'company',
            'location',
            'email',
            'blog',
            'bio'
        ]
        writer.writerow(keys)
        for user in users_with_data:
            def default(d, k):
                if d[k]:
                    return unicode(d[k])
                else:
                    return ''
            writer.writerow([default(user, key) for key in keys])

if __name__ == "__main__":
    start()
