#!/bin/bash

echo "BUILD START"

# create a virtual environment named 'venv' if it doesn't already exist
python3.9 -m venv venv

# activate the virtual environment
source venv/bin/activate

# install all dependencies in the venv
pip install -r requirements.txt

# delete old static files
echo "Deleting old static files..."
rm -rf staticfiles  # adjust path if needed (e.g., 'static' or 'app_name/static')

# collect static files using the Python interpreter from venv
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "BUILD END"
