#!/usr/bin/env bash
# exit on error
set -e

# Install dependencies
pip install -r requirements.txt

# Run build commands
python manage.py collectstatic --no-input
python manage.py migrate

# Create the superuser
# This command will fail if the user already exists.
echo "Creating superuser..."
python manage.py createsuperuser --noinput --username admin --email guptavishu1000@gmail.com