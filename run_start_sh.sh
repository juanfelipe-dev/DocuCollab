#!/bin/bash
# Entrypoint script for Render.com deployment

# Apply database migrations
python manage.py migrate --noinput

# Collect static files (if using static hosting)
python manage.py collectstatic --noinput

# Start the Django server (using gunicorn for production)
gunicorn docucollab.wsgi:application --bind 0.0.0.0:10000 --workers 3
