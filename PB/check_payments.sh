#!/bin/bash

source venv/bin/activate
torontofitnessclub/manage.py shell < check_payments.py
deactivate