from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date
from users.models import User
from core.models import Project
from core.models import Department
from api.serializers.serializers import DepartmentSerializer
from rest_framework.authtoken.models import Token

class DepartmentAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', user_name='testuser')
        self.token = Token.objects.create(user=self.user)
        self.project = Project.objects.create(project_name='Test Project', description='Test Description')
        self.department = Department.objects.create(
            department_name='Test Department',
            department_head=self.user,
            creation_date=date.today()
        )
        self.department.members.add(self.user)
        self.department.project.add(self.project)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get(self):
        url = '/api/v1/departments/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the retrieved departments data if needed
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_post(self):
        data = {
            'department_name': 'New Department',
            'department_head': self.user.id,
            'members': [self.user.id],
            'creation_date': str(date.today()),
            'project': [self.project.id],
        }
        url = '/api/v1/departments/'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the department is saved in the database
        department = Department.objects.get(department_name='New Department')
        self.assertEqual(department.department_head, self.user)
        self.assertIn(self.user, department.members.all())
        self.assertEqual(department.creation_date, date.today())
        self.assertIn(self.project, department.project.all())

    # def test_put(self):
    #     data = {
    #         'department_name': 'Updated Department',
    #         'department_head': self.user.id,
    #         'members': [self.user.id],
    #         'creation_date': str(date.today()),
    #         'project': [self.project.id],
    #     }
    #     url = f'/api/v1/departments/{self.department.id}/'
    #     response = self.client.put(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    #     # Verify the updated department data if needed
    #     self.department.refresh_from_db()
    #     self.assertEqual(self.department.department_name, 'Updated Department')

    # def test_delete(self):
    #     url = f'/api/v1/departments/{self.department.id}/'
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    #     # Verify that the department is no longer present in the database
    #     with self.assertRaises(Department.DoesNotExist):
    #         Department.objects.get(id=self.department.id)
