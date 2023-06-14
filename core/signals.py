from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.management import call_command
from core.management.commands.create_default_project_status import ProjectStatusCommand
from core.models import Project, ProjectStatus
from django.db import transaction

DEFAULT_PROJECT_STATUS = [
    {'name': 'Complete', 'color': '#00FF00', 'is_default': True},
    {'name': 'In Progress', 'color': '#A020F0', 'is_default': True},
    {'name': 'Inactive', 'color': '#FF0000', 'is_default': True},
    {'name': 'Not Yet Started', 'color': '#FFFF00', 'is_default': True}
]

@receiver(post_save, sender=Project)
def assign_default_project_status(sender, instance, created, **kwargs):
    # if created:
    #     call_command('create_default_project_status')
    
    if created:
        # with transaction.atomic():
        for status in DEFAULT_PROJECT_STATUS:
            name = status['name']
            color = status['color']
            is_default = status['is_default']
            ProjectStatus.objects.create(project=instance, name=name, color=color, is_default=is_default)

    # if created:
    #     create_default_project_status_command = ProjectStatusCommand()
    #     create_default_project_status_command.handle()

