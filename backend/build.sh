set -e
set -u
set -o pipefail

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
