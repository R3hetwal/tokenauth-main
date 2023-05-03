import random
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from core.models import Project
from celery import shared_task
from django.db.models.functions import TruncWeek, TruncMonth
from django.db.models import Count
from core.models import Project
# import os
# import json

@shared_task(
    # specifies that the task instance will be passed as the first argument to the task function. 
    # This is useful if you need access to the task instance within your function.
    bind=True,

    # specifies that the task should automatically retry in case of any exception.
    autoretry_for=(Exception,),

    # specifies the base time (in seconds) to wait before retrying the task. 
    # The actual time is increased exponentially with each retry.
    retry_backoff=5,

    # specifies whether to add a random amount of jitter to the retry wait time. 
    # This helps to prevent a large number of tasks from retrying at exactly the same time.
    retry_jitter=True,

    # specifies the maximum number of times the task should be retried in case of failure.
    retry_kwargs={"max_retries": 3},
)
def create_dummy_projects(self, num_projects):
    # Get the current time in UTC
    now = timezone.now()

    # Create dummy projects
    for i in range(num_projects):
        # Generate random project name
        project_name = f"Project {i + 1}"

        # Generate random deadline
        deadline = now + timedelta(days=random.randint(-365, 365))

        # Determine whether project is active or inactive
        complete = deadline > now

        # Get a random user as the project owner
        User = get_user_model()
        try:
            owner = User.objects.order_by("?").first()
        except ObjectDoesNotExist:
            owner = None

        # Create the project
        Project.objects.create(
            project_name=project_name,
            owner=owner,
            deadline=deadline,
            complete=complete,
        )

#Grouping the projects
@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_jitter=True,
    retry_kwargs={"max_retries": 3},
)
def group_dummy_projects(self):
    # Group projects by week and month
    projects_by_week = (
        Project.objects.exclude(start_date=None)
        .annotate(week=TruncWeek('start_date'))
        .values('week')
        .annotate(count=Count('id'))
    )

    projects_by_month = (
        Project.objects.exclude(start_date=None)
        .annotate(month=TruncMonth('start_date'))
        .values('month')
        .annotate(count=Count('id'))
    )

    # Response format for weekly grouping
    response_weekly = {}
    for project in projects_by_week:
        week_number = project['week'].strftime('%B_week_%W') if project['week'] is not None else 'None'
        response_weekly[week_number] = project['count']

    # Response format for monthly grouping
    response_monthly = {}
    for project in projects_by_month:
        month_number = project['month'].strftime('%B_%Y') if project['month'] is not None else 'None'
        response_monthly[month_number] = project['count']
    
    return {
        'weekly': response_weekly,
        'monthly': response_monthly,
    }



