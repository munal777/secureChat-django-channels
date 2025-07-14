#!/bin/bash
# Exit on error
set -o errexit

# Set Django settings module
export DJANGO_SETTINGS_MODULE=myproject.settings

echo "=== Starting deployment ==="
echo "DATABASE_URL: ${DATABASE_URL:-'Not set'}"
echo "REDIS_URL: ${REDIS_URL:-'Not set'}"
echo "DEBUG: ${DEBUG:-'Not set'}"
echo "ALLOWED_HOSTS: ${ALLOWED_HOSTS:-'Not set'}"
echo "============================"

# Check if required environment variables are set
if [ -z "$DATABASE_URL" ]; then
    echo "⚠️  WARNING: DATABASE_URL is not set!"
fi

if [ -z "$DJANGO_SECRET_KEY" ]; then
    echo "❌ ERROR: DJANGO_SECRET_KEY is not set!"
    exit 1
fi

# Function to run migrations with retry
run_migrations() {
    local max_retries=3
    local retry_count=0
    local wait_time=15
    
    while [ $retry_count -lt $max_retries ]; do
        echo "🔄 Running database migrations (attempt $((retry_count + 1))/$max_retries)..."
        
        if python manage.py migrate --noinput; then
            echo "✅ Database migrations completed successfully!"
            return 0
        else
            retry_count=$((retry_count + 1))
            if [ $retry_count -lt $max_retries ]; then
                echo "❌ Migration failed, waiting ${wait_time} seconds before retry..."
                sleep $wait_time
            else
                echo "❌ All migration attempts failed after $max_retries tries"
                return 1
            fi
        fi
    done
}

# Test Django settings
echo "🧪 Testing Django configuration..."
if python manage.py check --deploy; then
    echo "✅ Django configuration check passed!"
else
    echo "❌ Django configuration check failed!"
    exit 1
fi

# Run migrations
if ! run_migrations; then
    echo "Failed to run migrations. Exiting..."
    exit 1
fi

echo "🚀 Starting Django server on 0.0.0.0:${PORT}..."
daphne -b 0.0.0.0 -p ${PORT} myproject.asgi:application