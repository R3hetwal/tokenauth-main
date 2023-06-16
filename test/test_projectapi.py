from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from users.models import User
from core.models import Project

"""
    Unit test case for the ProjectViewSet.

    This test case verifies the behavior of the ProjectViewSet by testing various HTTP methods for project operations.

    Attributes:
        factory (APIRequestFactory): An instance of the APIRequestFactory used for creating test requests.

    Methods:
        setUp(): Set up the necessary objects and credentials for testing.
        test_list(): Test the GET request for retrieving a list of projects.
        test_retrieve(): Test the GET request for retrieving a specific project.
        test_create(): Test the POST request for creating a new project.
        test_update(): Test the PUT request for updating a specific project.
        test_delete(): Test the DELETE request for deleting a specific project.

"""

class ProjectViewSetTestCase(APITestCase):
    def setUp(self):
        """
        Set up the necessary objects and credentials for testing.

        This method initializes the APIRequestFactory for creating test requests.
        It creates a test user with the specified email and username.
        A token associated with the user is also created.
        The client's credentials are set with the authorization token.

        """
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            email='detective@gmail.com',
            user_name='thedetective'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_list(self):
        """
        Test the GET request for retrieving a list of projects.

        This method creates a GET request using the APIRequestFactory for the '/api/v1/projects/' URL.
        It also sends a GET request using the test client.

        The method asserts that the response status code is HTTP 200 OK, indicating a successful request.
        
        """
        url = '/api/v1/projects/'
        request = self.factory.get(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        """
        Test the GET request for retrieving a specific project.

        This method creates a test project with the specified project name and description.
        It constructs the URL for retrieving the project using the project's ID.
        The method then creates a GET request using the APIRequestFactory and sends another GET
        request using the test client.

        The method asserts that the response status code is HTTP 200 OK, indicating a successful request.

        """
        project = Project.objects.create(project_name='Test Project', description='Test Description')
        url = f'/api/v1/projects/{project.id}/'
        request = self.factory.get(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        """
        Test the POST request for creating a new project.

        This method creates a POST request using the APIRequestFactory for the '/api/v1/projects/' URL.
        It includes the necessary data for creating a new project, such as the project name and description.
        The method then sends a POST request using the test client with the provided data.

        The method asserts that the response status code is HTTP 201 CREATED, indicating a successful creation.
        
        """
        url = '/api/v1/projects/'
        data = {'project_name': 'New Project', 'description': 'New project description'}
        request = self.factory.post(url, data)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        """
        Test the PUT request for updating a specific project.

        This method creates a test project with the specified project name and description.
        It constructs the URL for updating the project using the project's ID.
        The method then creates a PUT request using the APIRequestFactory and sends another PUT
        request using the test client with the provided data for updating the project.

        The method asserts that the response status code is HTTP 200 OK, indicating a successful update.

        """
        project = Project.objects.create(project_name='Test Project', description='Test Description')
        url = f'/api/v1/projects/{project.id}/'
        data = {'project_name': 'Updated Project', 'description': 'Updated description'}
        request = self.factory.put(url, data)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update(self):
        """
        Test the PUT request for updating a specific project.

        This method creates a test project with the specified project name and description.
        It constructs the URL for updating the project using the project's ID.
        The method then creates a PUT request using the APIRequestFactory and sends another PUT
        request using the test client with the provided data for updating the project.

        The method asserts that the response status code is HTTP 200 OK, indicating a successful update.

        """
        project = Project.objects.create(project_name='Test Project', description='Test Description')
        url = f'/api/v1/projects/{project.id}/'
        data = {'description': 'Updated description testing'}
        request = self.factory.patch(url, data)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        """
        Test the DELETE request for deleting a specific project.

        This method creates a test project with the specified project name and description.
        It constructs the URL for deleting the project using the project's ID.
        The method then sends a DELETE request using the test client to the constructed URL.

        The method asserts that the response status code is HTTP 204 NO CONTENT, indicating a successful 
        deletion.

        Additionally, it verifies that the project is actually deleted by attempting to retrieve it again.
        It uses the `Project.DoesNotExist` exception to assert that the project no longer exists in the 
        database.

        """
        project = Project.objects.create(project_name='Test Project', description='Test Description')
        url = f'/api/v1/projects/{project.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify that the project is actually deleted
        with self.assertRaises(Project.DoesNotExist):
            Project.objects.get(id=project.id)

    

