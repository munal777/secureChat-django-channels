# Exit on error
set -o errexit

echo "Running database migrations..."
python manage.py migrate

echo "Starting Django server..."
daphne myproject.asgi:application