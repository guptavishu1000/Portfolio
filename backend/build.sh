#!/usr/bin/env bash
# exit on error
set -o errexit

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "📂 Collecting static files..."
python manage.py collectstatic --no-input

echo "🔎 Checking migrations status..."
python manage.py showmigrations portfolio_api || true

echo "🛠️ Applying migrations..."
# First try normally
if ! python manage.py migrate --no-input; then
  echo "⚠️ Migration failed, trying with --run-syncdb..."
  python manage.py migrate --run-syncdb --no-input
fi

echo "✅ Migrations applied. Current state:"
python manage.py showmigrations

echo "👤 Ensuring superuser exists..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
import os;
User = get_user_model();
username = os.getenv('DJANGO_SUPERUSER_USERNAME','admin');
password = os.getenv('DJANGO_SUPERUSER_PASSWORD','adminpass');
email = os.getenv('DJANGO_SUPERUSER_EMAIL','admin@example.com');
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username,password=password,email=email)
"

echo "👥 Listing users:"
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
print(list(User.objects.values('username','is_staff','is_superuser')))
"
