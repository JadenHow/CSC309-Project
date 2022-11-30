#!/bin/sh
source venv/bin/activate
pip3 install -r requirements.txt
python3 backend/manage.py makemigrations
python3 backend/manage.py migrate
