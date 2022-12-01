#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
torontofitnessclub/manage.py migrate
export DJANGO_SUPERUSER_EMAIL=admin@teach.cs.toronto.edu
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_PASSWORD=123
torontofitnessclub/manage.py createsuperuser --no-input
deactivate