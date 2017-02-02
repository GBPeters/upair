#!/usr/bin/env bash

export PGPASSWORD=maja

# Install postgres and postgis
echo "Installing PostgreSQL and PostGIS extension..."
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt xenial-pgdg main" >> /etc/apt/sources.list'
wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql-9.5-postgis-2.2 pgadmin3 postgresql-contrib-9.5

# Install setuptools and other dependencies
echo "Installing Python dependencies..."
sudo pip install --upgrade pip
sudo pip install setuptools
sudo pip install .

# Create database and tables
echo "Configuring database..."
sudo -u postgres psql -c "CREATE ROLE teammaja WITH LOGIN CREATEDB"
sudo -u postgres psql -c "ALTER ROLE teammaja WITH PASSWORD '$PGPASSWORD'"
psql -h localhost -U teammaja -d postgres -c "CREATE DATABASE upair"
sudo -u postgres psql -d upair -c "CREATE EXTENSION postgis;"
psql -h localhost -U teammaja -d upair -f sql/create_aircraft.sql
psql -h localhost -U teammaja -d upair -f sql/create_airways.sql
psql -h localhost -U teammaja -d upair -f sql/create_responses.sql
psql -h localhost -U teammaja -d upair -f sql/create_rtflightpaths.sql
psql -h localhost -U teammaja -d upair -f sql/create_rtstates.sql
psql -h localhost -U teammaja -d upair -f sql/create_states.sql

# Run instructions
echo "Install done."
echo "You should now be able to start up an opensky harvest bot using: "
echo "python bot/app.py opensky -i 60"