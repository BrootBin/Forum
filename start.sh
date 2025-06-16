#!/bin/bash

echo "Компіліруємо SCSS у CSS"
python manage.py compilescss

echo "Збираємо статичні файли"
python manage.py collectstatic --noinput

echo "Запускаємо Gunicorn"
gunicorn forum_project.wsgi:application --bind 0.0.0.0:$PORT
