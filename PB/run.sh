#!/bin/bash

source venv/bin/activate
export GOOGLE_MAPS_API_KEY=AIzaSyD_6PPzVleSevvSVbWN3P3v44uv36y59gs
torontofitnessclub/manage.py migrate
torontofitnessclub/manage.py runserver
deactivate