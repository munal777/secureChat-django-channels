#!/bin/bash

# Exit on error
set -o errexit

# Set Django settings module
export DJANGO_SETTINGS_MODULE=myproject.settings


python -c "
import os
import time
import psycopg2
from decouple import config

max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        conn = psycopg2.connect(
            host=config('DB_HOST'),
            port=config('DB_PORT'),
            user=config('DB_USER'),
            password=config('DB_PASSWORD'),
            database=config('DB_NAME')
        )
        conn.close()
        print('Database is ready!')
        break
    except psycopg2.OperationalError as e:
        retry_count += 1
        print(f'Database not ready, retrying... ({retry_count}/{max_retries})')
        time.sleep(2)

if retry_count >= max_retries:
    print('Failed to connect to database after maximum retries')
    exit(1)
"


echo "Running database migrations..."
python manage.py migrate

echo "Starting Django server on 0.0.0.0:${PORT}..."
daphne -b 0.0.0.0 -p ${PORT} myproject.asgi:application