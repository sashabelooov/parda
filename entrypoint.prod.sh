#!/bin/bash
set -e

echo "Starting Django application..."

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate

echo "Starting Gunicorn..."
gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120