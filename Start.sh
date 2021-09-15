#!/bin/bash

python /Data/manage.py makemigrations
python /Data/manage.py makemigrations ProxySearch
python /Data/manage.py migrate
python /Data/manage.py runserver 0.0.0.0:8000
