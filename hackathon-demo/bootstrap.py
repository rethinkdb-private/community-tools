import rethinkdb as r

conn = r.connect()

auth = {
    'type': 'basic',
    'user': '931518c4ba0f1648470cb933085ddc4f5b1409ed',
    'pass': '',
}

r.table_create('issues').run(conn)

r.table('issues').insert(
    r.http('https://api.github.com/repos/rethinkdb/rethinkdb/issues',
                  page='link-next',
                  page_limit=-1,
                  params={'per_page': 100, 'state': 'all' },
                  auth=auth,
       )
).run(conn)
