from django.core.management.base import BaseCommand
from core.models import Project, ProjectStatus

PROJECT_STATUS_LIST = [
    {'name': 'Complete', 'color': '#00FF00', 'is_default': True},
    {'name': 'In Progress', 'color': '#A020F0', 'is_default': True},
    {'name': 'Inactive', 'color': '#FF0000', 'is_default': True},
    {'name': 'Not Yet Started', 'color': '#FFFF00', 'is_default': True}
]

class ProjectStatusCommand(BaseCommand):
    help = 'Set Default Project Statuses'

    def handle(self, *args, **options):
        projects = Project.objects.all()

        # Create or retrieve all ProjectStatus objects
        for status in PROJECT_STATUS_LIST:
            name = status['name']
            color = status['color']
            is_default = status['is_default']

            # Assign the entire set of ProjectStatus instances to all projects
            
            print(projects)
            for project in projects:
                print('Ennter loop ::::::::::::::', project)

                project_status, created = ProjectStatus.objects.get_or_create(project=project, name=name, color=color, is_default=is_default)
                # project_statuses.append(project_status)
                # project.status_project.set(project_statuses) # Assign the entire set of project statuses to each project

                if created:
                    self.stdout.write(self.style.SUCCESS('Default Project Status option added successfully: "%s"' % project_status))
