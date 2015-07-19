from psycopg2 import connect

def create_streams_table(cur):
    columns = [
        'id serial primary key',
        'name text UNIQUE NOT NULL'
    ]
    cur.execute('CREATE TABLE streams ({})'.format(','.join(columns)))

def create_events_table(cur):
    columns = [
        'id uuid primary key default uuid_generate_v4()',
        'created_at timestamp default now() NOT NULL',
        'stream_id integer REFERENCES streams (id) NOT NULL',
        'data json'
    ]
    cur.execute('create extension "uuid-ossp"')
    cur.execute('CREATE TABLE events ({})'.format(','.join(columns)))

if __name__ == "__main__":
    con = connect(dbname='postgres',
                  user='postgres',
                  host='postgres',
                  password='')
    con.autocommit = True
    cur = con.cursor()

    create_streams_table(cur)
    create_events_table(cur)

    cur.close()
    con.close()
