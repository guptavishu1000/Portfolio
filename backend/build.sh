#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input


# Show existing migrations
echo "Showing existing migrations:"
python manage.py showmigrations

# Apply migrations with more verbosity
echo "Applying migrations..."
python manage.py migrate --no-input --fake-initial

# Show migrations after applying
echo "Migrations after applying:"
python manage.py showmigrations

echo "Listing Django users..."
python manage.py shell -c "from django.contrib.auth.models import User; print(list(User.objects.values('username','is_staff','is_superuser')))"

# Use our new, safe command that won't fail
python manage.py createsuperuser --noinput || true