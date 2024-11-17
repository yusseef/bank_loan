#!/bin/sh

# Exit script on error
set -e

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Starting server..."
exec "$@"
