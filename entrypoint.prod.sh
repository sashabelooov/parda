#!/bin/bash
set -e

echo "Starting Django application..."

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate

echo "Checking superuser"
python manage.py shell <<'PY'
from decouple import config
from django.contrib.auth import get_user_model
User = get_user_model()
username = config('DJANGO_SUPERUSER_USERNAME', default=None)
pwd   = config('DJANGO_SUPERUSER_PASSWORD', default=None)
if username and pwd and not User.objects.filter(username=username).exists():
    print(f"Creating superuser {username}...")
    User.objects.create_superuser(username=username, password=pwd)
    print("Superuser created.")
else:
    print("Superuser exists or env not provided; skipping.")
PY


echo "Starting Gunicorn..."
gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120

