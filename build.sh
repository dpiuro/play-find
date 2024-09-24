#!/usr/bin/env bash

# Exit on error
set -o errexit

pip install -r requirements.txt


echo "Шлях до Python:"
which python

echo "Змінна PATH:"
echo $PATH

python manage.py collectstatic --no-input

python manage.py migrate
