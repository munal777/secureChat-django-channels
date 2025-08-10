#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

python manage.py migrate --no-input

exec daphne -b 0.0.0.0 -p 8000 myproject.asgi:application