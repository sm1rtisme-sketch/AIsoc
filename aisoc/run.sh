#!/bin/bash
set -e

cd "$(dirname "$0")"

mkdir -p data logs tmp

pip install -r requirements.txt -q

python manage.py migrate --noinput

python manage.py runserver 0.0.0.0:8080
