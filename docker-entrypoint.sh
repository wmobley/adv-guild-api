#!/bin/bash
set -e

echo "Waiting for database to be ready..."

# Function to check if database is ready using Python
check_db() {
    python -c "
import psycopg2
import sys
import os
import time

db_url = os.environ.get('DATABASE_URL')
if not db_url:
    print('DATABASE_URL not set')
    sys.exit(1)

# Parse DATABASE_URL to get connection parameters
# Format: postgresql://user:password@host:port/database
import re
match = re.match(r'postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', db_url)
if not match:
    print('Invalid DATABASE_URL format')
    sys.exit(1)

user, password, host, port, database = match.groups()

try:
    conn = psycopg2.connect(
        host=host,
        port=int(port),
        user=user,
        password=password,
        database=database,
        connect_timeout=5
    )
    conn.close()
    print('Database connection successful')
    sys.exit(0)
except Exception as e:
    print(f'Database connection failed: {e}')
    sys.exit(1)
"
}

# Wait for database to be ready (max 60 seconds)
for i in {1..60}; do
    if check_db; then
        echo "Database is ready!"
        break
    fi
    echo "Waiting for database... (attempt $i/60)"
    sleep 1
done

if ! check_db; then
    echo "Database failed to become ready after 60 seconds"
    exit 1
fi

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

echo "Starting application..."
exec "$@"
