#!/bin/sh
set -e

# Run migrations and collectstatic then start the server
# Use a short sleep to wait for DB availability if necessary (optional)

# If you use env var WAIT_FOR_DB, you can implement a wait-for-db loop here

python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Exec the CMD from Dockerfile to run gunicorn
exec "$@"