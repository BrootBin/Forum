#!/bin/bash

echo "Компіліруємо SCSS у CSS"
python3 manage.py compilescss

echo "Збираємо статичні файли"
python3 manage.py collectstatic --noinput

echo "Запускаємо Gunicorn"
gunicorn forum_project.wsgi:application --bind 0.0.0.0:$PORT