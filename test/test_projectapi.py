from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.authtoken.models import Token
from rest_framework import status
from users.models import User
from core.models import Project


class ProjectViewSetTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            email='detective@gmail.com',
            user_name='thedetective'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_list(self):
        url = '/api/v1/projects/'
        request = self.factory.get(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        project = Project.objects.create(project_name='Test Project', description='Test Description')
        url = f'/api/v1/projects/{project.id}/'
        request = self.factory.get(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        url = '/api/v1/projects/'
        data = {'project_name': 'New Project', 'description': 'New project description'}
        request = self.factory.post(url, data)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        project = Project.objects.create(project_name='Test Project', description='Test Description')
        url = f'/api/v1/projects/{project.id}/'
        data = {'project_name': 'Updated Project', 'description': 'Updated description'}
        request = self.factory.put(url, data)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update(self):
        project = Project.objects.create(project_name='Test Project', description='Test Description')
        url = f'/api/v1/projects/{project.id}/'
        data = {'description': 'Updated description testing'}
        request = self.factory.patch(url, data)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_delete(self):
    #     project = Project.objects.create(project_name='Test Project', description='Test Description')
    #     url = f'/api/v1/projects/{project.id}/'
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    #     # Verify that the project is actually deleted
    #     with self.assertRaises(Project.DoesNotExist):
    #         Project.objects.get(id=project.id)

    

