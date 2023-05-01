from celery import shared_task
from datetime import date
from users.models import User
from core.models import Project
from core.celery_models import SummaryData

@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_jitter=True,
    retry_kwargs={"max_retries": 3},
)
def update_summary_data(self):
    today = date.today()
    month = today.month
    year = today.year
    total_projects = Project.objects.count()
    total_users = User.objects.count()

    summary_data, created = SummaryData.objects.get_or_create(month=month, year=year)
    summary_data.total_projects = total_projects
    summary_data.total_users = total_users

    summary_data.total_projects = total_projects if total_projects else 0
    summary_data.total_users = total_users if total_users else 0

    summary_data.save()

@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_jitter=True,
    retry_kwargs={"max_retries": 3},
)
def print_data(self):
    print("Celery Running successfully!")