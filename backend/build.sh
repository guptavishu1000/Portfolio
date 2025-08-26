#!/usr/bin/env bash
# exit on error
set -e
set -u
set -o pipefail

# Install dependencies
pip install -r requirements.txt

# Run build commands
python manage.py collectstatic --no-input

# (Optional) Create a superuser if the environment variable is set
if [[ -n "${CREATE_SUPERUSER-}" ]]; then
  echo "Creating superuser..."
  python manage.py createsuperuser --no-input
fi