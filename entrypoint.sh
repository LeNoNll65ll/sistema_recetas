#!/bin/sh

echo 'Running collecstatic...'
python manage.py collectstatic --no-input --settings=recetas.settings.production

echo 'Applying migrations...'
python manage.py wait_for_db --settings=recetas.settings.production
python manage.py makemigrations --settings=recetas.settings.production
python manage.py migrate --settings=recetas.settings.production

echo 'Running server...'
gunicorn --env DJANGO_SETTINGS_MODULE=recetas.settings.production recetas.wsgi:application --bind 0.0.0.0:8000 --workers=2