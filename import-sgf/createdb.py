from psycopg2 import connect

if __name__ == "__main__":
    con = connect(dbname='postgres',
                  user='postgres',
                  host='postgres',
                  password='')
    con.autocommit = True
    cur = con.cursor()

    columns = [
        'id serial primary key',
        'name text NOT NULL'
    ]
    cur.execute('CREATE TABLE streams ({})'.format(','.join(columns)))

    columns = [
        'id uuid primary key default uuid_generate_v4()',
        'created_at timestamp default now() NOT NULL',
        'stream_id integer REFERENCES streams (id) NOT NULL',
        'data json'
    ]
    cur.execute('create extension "uuid-ossp"')
    cur.execute('CREATE TABLE events ({})'.format(','.join(columns)))

    cur.close()
    con.close()
