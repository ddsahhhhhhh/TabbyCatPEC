#!/usr/bin/env bash
# exit on error
set -o errexit

echo "-----> Install dependencies"
python -m pip install pipenv
pipenv install --system --ignore-pipfile

echo "-----> Running database migration"
python manage.py migrate --noinput

echo "-----> Running dynamic preferences checks"
python manage.py checkpreferences

echo "-----> Running static asset compilation"
npm ci --only=production
npm run build

echo "-----> Running static files compilation"
python manage.py collectstatic --noinput

echo "-----> Post-compile done"
