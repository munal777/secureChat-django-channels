# Exit on error
set -o errexit

# Set Django settings module
export DJANGO_SETTINGS_MODULE=myproject.settings


echo "Running database migrations..."
python manage.py migrate

echo "Starting Django server..."

PORT=${PORT:-8000}
daphne -b 0.0.0.0 -p $PORT myproject.asgi:application