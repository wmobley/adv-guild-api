#!/bin/bash
set -e

# Define the test database name, using a default if not set
TEST_DB_NAME=${POSTGRES_DB_TEST:-quest_db_test}

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create the test database if it doesn't exist and grant privileges
    SELECT 'CREATE DATABASE ' || quote_ident('$TEST_DB_NAME')
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$TEST_DB_NAME')\gexec
    GRANT ALL PRIVILEGES ON DATABASE "$TEST_DB_NAME" TO "$POSTGRES_USER";
EOSQL