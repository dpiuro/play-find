#!/usr/bin/env bash

# Exit on error
set -o errexit

# Установити залежності
pip install -r requirements.txt

python --version

# Збираємо статичні файли
python manage.py collectstatic --no-input

# Виконуємо міграції
python manage.py migrate
