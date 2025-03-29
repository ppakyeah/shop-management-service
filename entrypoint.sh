#!/bin/sh

echo "Running Database Migrations"
python manage.py makemigrations
python manage.py migrate

echo "Running product management commands"
python manage.py init_data

exec "$@"