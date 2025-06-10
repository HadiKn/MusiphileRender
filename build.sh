#!/usr/bin/env bash
# Exit on error
set -o errexit

# Apply any outstanding database migrations
python manage.py migrate --no-input

# Collect static files
python manage.py collectstatic --no-input --clear