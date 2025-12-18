Quick deploy checklist for Render

1. Add env vars in Render dashboard (Service -> Environment):
   - SECRET_KEY (required)
   - DEBUG (set to False)
   - ALLOWED_HOSTS (comma-separated domain(s))
   - DATABASE_URL (Render managed Postgres or other)
   - MEDIA_URL (optional, default `/curtains/`)
   - MEDIA_ROOT (optional, where uploaded files will be stored on render disk)

2. Hook up repo on Render and configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn core.wsgi --bind 0.0.0.0:$PORT --workers 3`
   - Release Command: `python manage.py migrate && python manage.py collectstatic --noinput`

3. (Optional) Use S3 for media: install `boto3` and `django-storages`, set S3 env vars and update settings to use `storages.backends.s3boto3.S3Boto3Storage`.

Additional env vars you can use:
- USE_S3=True to enable S3 media storage
- AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME (for S3)
- WAIT_FOR_DB=1 to make the container wait for the database to become available before running migrations

4. Verify logs, health, and run `python manage.py createsuperuser` if you need an admin user.
