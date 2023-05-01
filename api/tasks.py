import random
import pytz
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from core.models import Project
from celery import shared_task
from django.db.models.functions import TruncWeek, TruncMonth
from django.db.models import Count
from core.models import Project
import os
import json


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_jitter=True,
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

    # Example response format for weekly grouping
    response_weekly = {}
    for project in projects_by_week:
        week_number = project['week'].strftime('%B_week_%W') if project['week'] is not None else 'None'
        response_weekly[week_number] = project['count']

    # Example response format for monthly grouping
    response_monthly = {}
    for project in projects_by_month:
        month_number = project['month'].strftime('%B_%Y') if project['month'] is not None else 'None'
        response_monthly[month_number] = project['count']
    
    return {
        'weekly': response_weekly,
        'monthly': response_monthly,
    }



