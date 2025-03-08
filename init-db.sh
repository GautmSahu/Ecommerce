#!/bin/bash

# Connect to PostgreSQL and create the database
psql -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE $DATABASE_NAME;"
psql -U "$POSTGRES_USER" -d postgres -c "CREATE USER $DATABASE_USER WITH PASSWORD '$DATABASE_PASSWORD';"
psql -U "$POSTGRES_USER" -d postgres -c "ALTER ROLE $DATABASE_USER SET client_encoding TO 'utf8'; "
psql -U "$POSTGRES_USER" -d postgres -c "ALTER ROLE $DATABASE_USER SET default_transaction_isolation TO 'read committed'; "
psql -U "$POSTGRES_USER" -d postgres -c "ALTER ROLE $DATABASE_USER SET timezone TO 'UTC';"
psql -U "$POSTGRES_USER" -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DATABASE_NAME TO $DATABASE_USER;"
psql -U "$POSTGRES_USER" -d postgres -c "\c $DATABASE_NAME;" -c "ALTER ROLE $DATABASE_USER SET search_path TO public;" -c "GRANT USAGE ON SCHEMA public TO $DATABASE_USER;" -c "GRANT CREATE ON SCHEMA public TO $DATABASE_USER;"
echo "Database $POSTGRES_DB created successfully."
