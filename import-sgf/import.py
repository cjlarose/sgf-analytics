import fnmatch
import os
import uuid

import psycopg2
import psycopg2.extras

def sgf_files():
    parent = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'sgf')
    for root, dirnames, filenames in os.walk(parent):
        for filename in fnmatch.filter(filenames, '*.sgf'):
            yield os.path.join(root, filename)

def raw_sgf_events(filenames):
    for sgf_filename in filenames:
        f = open(sgf_filename, 'r')
        data = {
            'filename': os.path.basename(sgf_filename),
            'contents': f.read()
        }
        yield data

def save_event(cursor, id, stream_id, data):
    row = (str(id), stream_id, psycopg2.extras.Json(data))
    try:
        cursor.execute("INSERT INTO events (id, stream_id, data) VALUES (%s, %s, %s)", row)
    except psycopg2.IntegrityError:
        print("DETECTED DUPLICATE for event id {}".format(id))

def get_stream_id(cursor, stream_name):
    cursor.execute("SELECT id FROM streams WHERE name = %s", (stream_name,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO streams (name) VALUES (%s) RETURNING id",
                       (stream_name,))
        result = cursor.fetchone()
    return result[0]

def save_events(cursor, events):
    ns = uuid.UUID('154a6113-5503-45c2-90f6-030393f91d43')
    stream_id = get_stream_id(cursor, 'raw_sgf')

    for event in events:
        id = uuid.uuid5(ns, event['contents'])
        save_event(cursor, id, stream_id, event)

if __name__ == "__main__":
    con = psycopg2.connect(dbname='postgres',
                           user='postgres',
                           host='postgres',
                           password='')
    con.autocommit = True
    cursor = con.cursor()

    filenames = sgf_files()
    events = raw_sgf_events(filenames)
    save_events(cursor, events)

    cursor.close()
    con.close()
