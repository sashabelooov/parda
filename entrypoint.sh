#!/bin/sh
set -e

# Optional: wait for DB to become available before running migrations.
# Set WAIT_FOR_DB=1 and ensure DATABASE_URL is set in the environment.
if [ "${WAIT_FOR_DB:-0}" = "1" ]; then
  echo "Waiting for DB to become available..."
  python - <<'PY'
import os
import sys
import time
import urllib.parse
try:
    import psycopg2
except Exception:
    print('psycopg2 not available, skipping DB wait')
    sys.exit(0)

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    print('No DATABASE_URL, skipping DB wait')
    sys.exit(0)

url = urllib.parse.urlparse(DATABASE_URL)
user = url.username
password = url.password
dbname = url.path.lstrip('/')
host = url.hostname
port = url.port or 5432

for i in range(30):
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.close()
        print('DB is available')
        sys.exit(0)
    except Exception as exc:
        print('DB not ready, retrying...', str(exc))
        time.sleep(2)
print('DB still not available after retries, continuing')
PY
fi

python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Create a default superuser if env var CREATE_DEFAULT_SUPERUSER is set and no superuser exists (idempotent).
# Credentials: username=admin, password=12, email=admin@example.com
if [ "${CREATE_DEFAULT_SUPERUSER:-0}" = "1" ] || [ "${CREATE_DEFAULT_SUPERUSER:-0}" = "true" ]; then
  python - <<'PY'
from django.contrib.auth import get_user_model
import os
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('No superuser found; creating default admin user')
    username = os.environ.get('DEFAULT_SUPERUSER_USERNAME', 'admin')
    password = os.environ.get('DEFAULT_SUPERUSER_PASSWORD', '12')
    email = os.environ.get('DEFAULT_SUPERUSER_EMAIL', 'admin@example.com')
    User.objects.create_superuser(username, email, password)
else:
    print('Superuser already exists; skipping default admin creation')
PY
else
  echo "CREATE_DEFAULT_SUPERUSER not set; skipping default admin creation"
fi

# Run import_excel management command if the Excel file exists
if [ -f data/ОСТАТКИ.xlsx ]; then
  echo "Found Excel file; running python manage.py import_excel"
  python manage.py import_excel || echo "Import failed or returned non-zero; continuing"
else
  echo "No Excel file found at data/ОСТАТКИ.xlsx; skipping import"
fi

# Exec the CMD from Dockerfile (gunicorn)
exec "$@"