First, create the initial database. Because of timing issues, this command
may fail the first name. Just run it again.

```
docker-compose run --entrypoint python import ./createdb.py
```

If you want to take a look into postgres:

```
docker run -it --link sgfanalysis_postgres_1:postgres --rm postgres \
  sh -c 'exec psql -h "$POSTGRES_PORT_5432_TCP_ADDR" -p "$POSTGRES_PORT_5432_TCP_PORT" -U postgres'
```
