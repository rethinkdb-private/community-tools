#!/usr/bin/env python

import ucsv, requests, json, argparse, pprint
from multiprocessing import Pool
import datetime

GITHUB_TOKEN = '3df11993e5fa5e4b0c661b7abc965345f028c04d'
REPO = 'rethinkdb/rethinkdb'
headers = {
    'Authorization': 'token ' + GITHUB_TOKEN,
}
BLACKLIST = [login.lower() for login in ['mlucy', 'srh', 'danielmewes', 'coffeemug', 'JoeyZwicker', 'atnnn', 'Tryneus', 'jdoliner', 'KittyBot', 'ahruygt', 'mglukhovsky', 'neumino', 'wmrowan', 'al3xandru', 'timmaxw', 'rntz', 'frank-trampe', 'axc', 'larkost']]

def get_issue_comments(data):
    issue_title = data['issue_title']
    url = data['url']
    print "Fetching comments: "+url
    req = requests.get(url, headers=headers)
    if req.status_code is not 200:
        print "HTTP %d when looking up comments: %s" % (req.status_code, url)
    comments = json.loads(req.text)

    # Attach the issue title to each comment
    for comment in comments:
        comment['issue_title'] = issue_title

    return comments

def start():
    # Command-line argument: specify the CSV data file
    parser = argparse.ArgumentParser(description='Exports GitHub issue data to a CSV')
    parser.add_argument('csv', help='the CSV data file to write to')
    args = parser.parse_args()

    issues = []
    url = "https://api.github.com/repos/%s/issues?state=all&per_page=100" % REPO
    page_num = 0
    while True:
        req = requests.get(url, headers=headers)
        print "Fetching page %d of issues from %s" % (page_num + 1, REPO)
        issues = issues + json.loads(req.text)
        try:
            url = req.links['next']['url']
        except KeyError:
            break
        page_num = page_num + 1

    issue_comment_urls = []
    for issue in issues:
        issue_comment_urls.append({
            'issue_title': issue['title'],
            'url': issue['comments_url'],
        })


    # Look up comments for each issue
    p = Pool(5)
    issue_comments = p.map(get_issue_comments, issue_comment_urls)

    # Flatten the list of comments
    issue_comments = [comment for comments in issue_comments for comment in comments]

    # Order our issue and comment events by date time
    events = []
    for issue in issues:
        if issue['user']['login'].lower() not in BLACKLIST:
            events.append([issue['created_at'], 'opened_issue', issue['user']['login'], issue['html_url'], str(issue['number']), issue['title'], issue['body']])
    for comment in issue_comments:
        if comment['user']['login'].lower() not in BLACKLIST:
            issue_num = comment['issue_url'].rsplit('/', 1)[1]
            events.append([comment['created_at'], 'added_comment', comment['user']['login'], comment['html_url'], issue_num, comment['issue_title'], comment['body']])
    events.sort(key=lambda x: x[0])


    with open(args.csv, 'wb') as f:
        writer = ucsv.UnicodeWriter(f)
        writer.writerow(['timestamp', 'event', 'user', 'permalink', 'issue', 'issue_title', 'body'])
        for event in events:
            writer.writerow(event)

    print "Fetched %d events as of %s" % (len(events), datetime.datetime.now())

if __name__ == "__main__":
    start()
