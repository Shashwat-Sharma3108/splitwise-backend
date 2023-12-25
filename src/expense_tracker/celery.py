from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')

app = Celery('expense_tracker')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Configure Celery Beat schedule
app.conf.beat_schedule = {
    'send-weekly-expenditure-summary': {
        'task': 'expenses.tasks.send_weekly_expenditure_summary',
        'schedule': crontab(day_of_week='sunday', hour=0, minute=0),  # Run every Sunday at midnight
    },
}

app.conf.timezone = 'UTC'