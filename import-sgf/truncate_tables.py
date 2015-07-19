from psycopg2 import connect

if __name__ == "__main__":
    con = connect(dbname='postgres',
                  user='postgres',
                  host='postgres',
                  password='')
    con.autocommit = True
    cur = con.cursor()

    cur.execute('TRUNCATE TABLE streams CASCADE;');

    cur.close()
    con.close()
