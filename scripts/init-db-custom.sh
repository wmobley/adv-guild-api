#!/bin/bash
set -e

# Create test database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE $POSTGRES_DB_TEST;
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB_TEST TO $POSTGRES_USER;
EOSQL

# Setup main database with minimal PostGIS
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS postgis;
EOSQL

# Setup test database with minimal PostGIS
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB_TEST" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS postgis;
EOSQL

