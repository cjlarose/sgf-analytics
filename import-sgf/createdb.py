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

def create_trigger_fn(cur):
    fn_source = """
    CREATE FUNCTION notify_trigger() RETURNS trigger AS $$
    DECLARE
    BEGIN
      PERFORM pg_notify('new_event', CAST(NEW.id AS varchar(50)));
      PERFORM pg_notify('new_event_' || NEW.stream_id, CAST(NEW.id AS varchar(50)));
      RETURN new;
    END;
    $$ LANGUAGE plpgsql;
    """
    cur.execute(fn_source)

    trigger_source = """
    CREATE TRIGGER watched_table_trigger AFTER INSERT ON events
    FOR EACH ROW EXECUTE PROCEDURE notify_trigger();
    """
    cur.execute(trigger_source)

if __name__ == "__main__":
    con = connect(dbname='postgres',
                  user='postgres',
                  host='postgres',
                  password='')
    con.autocommit = True
    cur = con.cursor()

    create_streams_table(cur)
    create_events_table(cur)
    create_trigger_fn(cur)

    cur.close()
    con.close()
