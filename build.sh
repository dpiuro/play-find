#!/usr/bin/env bash

# Exit on error
set -o errexit

# Удаляємо та перевстановлюємо gunicorn
pip uninstall gunicorn -y && pip install gunicorn

# Установити залежності
pip install -r requirements.txt

# Збираємо статичні файли
python manage.py collectstatic --no-input

# Виконуємо міграції
python manage.py migrate
