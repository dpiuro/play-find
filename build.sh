#!/usr/bin/env bash

# Додаємо Python в PATH
export PATH="/opt/render/project/python/bin:$PATH"

# Exit on error
set -o errexit

# Установити залежності
pip install -r requirements.txt

# Встановити Gunicorn
pip install gunicorn

# Зібрати статичні файли
python manage.py collectstatic --no-input

# Виконати міграції
python manage.py migrate
