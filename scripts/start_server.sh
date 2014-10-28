#!/bin/bash
cd ../server_proj
. bin/activate
python manage.py runserver 0.0.0.0:8001
