# Exit on error
set -o errexit

# Set Django settings module
export DJANGO_SETTINGS_MODULE=myproject.settings


echo "Running database migrations..."
python manage.py migrate

echo "Starting Django server..."
daphne myproject.asgi:application