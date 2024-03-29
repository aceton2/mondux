#!/bin/sh

while ! nc -z $API_DB_HOST 5432 ; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up - executing command"

exec "$@"
