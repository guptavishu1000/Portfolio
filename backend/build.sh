#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input


# Show existing migrations
echo "Checking applied migrations..."
python manage.py showmigrations portfolio_api

echo "SQL for 0001_initial (just for reference):"
python manage.py sqlmigrate portfolio_api 0001_initial

# Apply migrations with more verbosity
echo "Applying migrations..."
python manage.py migrate --no-input

# Show migrations after applying
echo "Migrations after applying:"
python manage.py showmigrations

echo "Listing Django users..."
python manage.py shell -c "from django.contrib.auth.models import User; print(list(User.objects.values('username','is_staff','is_superuser')))"

echo "Ensuring superuser exists..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); \
import os; username=os.getenv('DJANGO_SUPERUSER_USERNAME','admin'); \
password=os.getenv('DJANGO_SUPERUSER_PASSWORD','adminpass'); \
email=os.getenv('DJANGO_SUPERUSER_EMAIL','admin@example.com'); \
\
(User.objects.filter(username=username).exists() or \
 User.objects.create_superuser(username=username,password=password,email=email))"