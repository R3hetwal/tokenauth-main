import os
import sys
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
# app.conf.enable_utc = False

# app.conf.update(timezone = 'Asia/Kathmandu')

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()


# Celery Schedules - https://docs.celeryproject.org/en/stable/reference/celery.schedules.html
app.conf.beat_schedule = {
    'update_summary_data': {
        'task': 'core.tasks.update_summary_data',
        'schedule': crontab(hour=6, minute=31),
    },  
    "create_dummy_projects": {
        "task": "api.tasks.create_dummy_projects",
        "schedule": crontab(hour=6, minute=32),
        "args": (100000,),  # Create 100000 dummy projects
    },
    "group_dummy_projects": {
        "task": "api.tasks.group_dummy_projects",
        "schedule": crontab(hour=6, minute=32),
    }
}

# Ensure that Celery is started with the --beat flag
if "beat" in sys.argv:
    app.conf.update(
        timezone=settings.TIME_ZONE,
        enable_utc=True,
    )

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')