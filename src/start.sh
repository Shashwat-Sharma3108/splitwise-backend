#!/bin/bash

# Start Redis server
redis-server &

# Start Celery Beat
celery -A expense_tracker.celery beat -l info &

# Start Celery Worker
celery -A expense_tracker.celery worker -l info &

# Create and activate Python virtual environment
python3 -m venv task
source task/bin/activate

# Install additional Python dependencies
pip3 install -r requirements.txt

# Apply migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Run Django development server
python3 manage.py runserver