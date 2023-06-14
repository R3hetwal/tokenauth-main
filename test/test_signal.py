from django.test import TestCase
from users.models import User
from core.models import Project, ProjectStatus
from django.db.models.signals import post_save

DEFAULT_PROJECT_STATUS = [
    {'name': 'Complete', 'color': '#00FF00', 'is_default': True},
    {'name': 'In Progress', 'color': '#A020F0', 'is_default': True},
    {'name': 'Inactive', 'color': '#FF0000', 'is_default': True},
    {'name': 'Not Yet Started', 'color': '#FFFF00', 'is_default': True}
]

class ProjectSignalTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user( 
            email='detective01@gmail.com',
            user_name='thedetective01',
            first_name='Waston',
            password='Waston1212*'
        )
    
    def test_assign_default_project_status(self):
        project = Project.objects.create(project_name='Test Project', owner=self.user)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(ProjectStatus.objects.count(), len(DEFAULT_PROJECT_STATUS))
        
        for status in DEFAULT_PROJECT_STATUS:
            self.assertTrue(ProjectStatus.objects.filter(
                project=project,
                name=status['name'],
                color=status['color'],
                is_default=status['is_default']
            ).exists())
