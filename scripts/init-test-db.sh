#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create the test database if it doesn't exist
    SELECT 'CREATE DATABASE ${POSTGRES_DB_TEST:-quest_db_test}'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '${POSTGRES_DB_TEST:-quest_db_test}')\gexec
EOSQL