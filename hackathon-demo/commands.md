RethinkDB is an open-source distributed JSON document database with
a pleasant and powerful query language called ReQL. To show off
ReQL, we'll explore the GitHub API. Let's look at the issues for the RethinkDB
GitHub repo.

Get a JSON document from the web using HTTP:
```
r.http('https://api.github.com/repos/rethinkdb/rethinkdb/issues')
```

See what data is in the table:

```
r.table('issues').limit(1)
```

Count the open issues:

```
r.table('issues').filter({'state': 'open'}).count()
```

See who has the most issues assigned to them:

```
r.table('issues')
    .filter({'state': 'open'})
    .group(function(issue) {
        return issue('assignee')('login');
    })
    .count()
```
