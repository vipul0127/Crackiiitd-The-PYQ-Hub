#!/bin/bash

echo "Starting build process..."

# Install dependencies
pip install -r requirements.txt

# Run migrations (optional, only if your app requires database migrations during deployment)
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

echo "Build process completed."
