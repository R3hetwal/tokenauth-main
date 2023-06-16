from django.test import TestCase
from users.models import User
from core.models import Project, ProjectStatus
from django.db.models.signals import post_save

"""
    Unit test case for project signals in Django.

    This test case verifies the behavior of project signals by assigning default project statuses to a project.

    Attributes:
        DEFAULT_PROJECT_STATUS (list): A list of dictionaries representing the default project statuses, each containing the status name, color, and default flag.

    Methods:
        setUp(): Set up the necessary test data, including creating a test user.
        test_assign_default_project_status(): Test the assignment of default project statuses to a project.

"""

DEFAULT_PROJECT_STATUS = [
    {'name': 'Complete', 'color': '#00FF00', 'is_default': True},
    {'name': 'In Progress', 'color': '#A020F0', 'is_default': True},
    {'name': 'Inactive', 'color': '#FF0000', 'is_default': True},
    {'name': 'Not Yet Started', 'color': '#FFFF00', 'is_default': True}
]

class ProjectSignalTestCase(TestCase):
    def setUp(self):
        """
            Set up the necessary test data.

            This method creates a test user with the following information:
            - Email: 'detective01@gmail.com'
            - Username: 'thedetective01'
            - First name: 'Waston'
            - Password: 'Waston1212*'

            This test user is assigned to the instance variable 'self.user' for use in test cases.
        """
        self.user = User.objects.create_user( 
            email='detective01@gmail.com',
            user_name='thedetective01',
            first_name='Waston',
            password='Waston1212*'
        )
    
    def test_assign_default_project_status(self):
        """
            Create a test project and verify default project statuses.

            This block of code performs the following actions:
            1. Creates a test project with the project name 'Test Project' and the owner set to 'self.user'.
            2. Asserts that there is only one project object in the database.
            3. Asserts that the number of project status objects in the database is equal to the length of the 
               'DEFAULT_PROJECT_STATUS' list.
            4. Iterates over each default project status in the 'DEFAULT_PROJECT_STATUS' list and verifies that 
               a corresponding project status object exists in the database for the created project.

            Note: The 'DEFAULT_PROJECT_STATUS' list contains dictionaries with the following keys: 'name', 'color', and 'is_default'.
        """
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
