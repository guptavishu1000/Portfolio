#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

echo "Listing Django users..."
python manage.py shell -c "from django.contrib.auth.models import User; print(list(User.objects.values('username','is_staff','is_superuser')))"

# Use our new, safe command that won't fail
python manage.py createsuperuser --noinput || true