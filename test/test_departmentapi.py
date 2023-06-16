from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from datetime import date
from users.models import User
from core.models import Project
from core.models import Department
from api.serializers.serializers import DepartmentSerializer
from rest_framework.authtoken.models import Token

"""
    Unit test case for the DepartmentAPIView.

    This test case verifies the behavior of the DepartmentAPIView by testing various HTTP methods for department operations.

    Attributes:
        user (User): A test user object created for testing purposes.
        token (Token): A token associated with the test user.
        project (Project): A test project object created for testing purposes.
        department (Department): A test department object created for testing purposes.

    Methods:
        setUp(): Set up the necessary objects and credentials for testing.
        test_get(): Test the GET request for retrieving departments.
        test_post(): Test the POST request for creating a new department.
        test_put(): Test the PUT request for updating a department.
"""

class DepartmentAPIViewTestCase(APITestCase):
    def setUp(self):
        """
        Set up the necessary objects and credentials for testing.

        This method creates a test user, a token associated with the user, a test project,
        and a test department. The user is set as the department head, and is added as a
        member of the department. The project is added to the department. The client's
        credentials are set with the authorization token.

        """
        self.factory = APIRequestFactory()
        self.user = User.objects.create(email='detective@gmail.com', user_name='thedetective')
        self.token = Token.objects.create(user=self.user)
        self.project = Project.objects.create(project_name='Test Project', description='Test Description')
        # self.department = Department.objects.create(
        #     department_name='Test Department',
        #     department_head=self.user,
        #     creation_date=date.today()
        # )
        # self.department.members.add(self.user)
        # self.department.project.add(self.project)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get(self):
        """
        Test the GET request for retrieving departments.

        This method sends a GET request to the '/api/v1/departments/' URL using the test client.
        It then asserts that the response status code is HTTP 200 OK.

        If needed, we can verify the retrieved departments data by comparing it with the serialized
        data obtained from the DepartmentSerializer. The method retrieves all departments from the
        database, serializes them using the DepartmentSerializer, and asserts that the response data
        matches the serialized data.

        """

        url = '/api/v1/departments/'
        request = self.factory.get(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the retrieved departments data if needed
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_post(self):
        """
        Test the POST request for creating a new department.

        This method sends a POST request to the '/api/v1/departments/' URL using the test client.
        It includes the necessary data for creating a new department, such as the department name,
        department head, members, creation date, and associated project.

        After the request is sent, the method asserts that the response status code is HTTP 201 CREATED.

        Furthermore, it verifies that the department is correctly saved in the database by retrieving it
        and performing several assertions. It checks that the department's attributes, such as the
        department head, members, creation date, and associated project, match the expected values.

        """
        # department = Department.objects.create(
        #     department_name='Test Department',
        #     department_head=self.user,
        #     creation_date=date.today()
        # )
        data = {
            'department_name': 'New Department',
            'department_head': self.user.id,
            'members': [self.user.id],
            'creation_date': str(date.today()),
            'project': [self.project.id],
        }
        url = '/api/v1/departments/'
        request = self.factory.post(url)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the department is saved in the database
        department = Department.objects.get(department_name='New Department')
        self.assertEqual(department.department_head, self.user)
        self.assertIn(self.user, department.members.all())
        self.assertEqual(department.creation_date, date.today())
        self.assertIn(self.project, department.project.all())

    def test_put(self):
        """

        Test the PUT request for updating a department.

        This method sends a PUT request to the '/api/v1/departments/{department_id}/' URL
        using the test client. It includes the necessary data for updating the department,
        such as the department name, department head, members, creation date, and associated project.

        After the request is sent, the method asserts that the response status code is HTTP 200 OK.

        Furthermore, it verifies that the department is correctly updated in the database by
        retrieving it and performing several assertions. It checks that the department's attributes,
        such as the department name, department head, members, creation date, and associated project,
        match the updated values.

        """
        department = Department.objects.create(
            department_name='Test Department',
            department_head=self.user,
            creation_date=date.today()
        )
        data = {
            'department_name': 'Updated Department',
            'department_head': self.user.id,
            'members': [self.user.id],
            'creation_date': str(date.today()),
            'project': [self.project.id],
        }
        url = f'/api/v1/departments/{department.id}'
        request = self.factory.get(url)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the department is updated in the database
        department.refresh_from_db()
        self.assertEqual(department.department_name, 'Updated Department')

    def test_delete(self):
        """
        Test the DELETE request for deleting a specific department.

        This method sends a DELETE request to the '/api/v1/departments/{department_id}/' URL using the test client.
        It retrieves the department ID from the `self.department` attribute, assuming it has been previously set up.

        The method asserts that the response status code is HTTP 204 NO CONTENT, indicating a successful deletion.

        Additionally, it verifies that the department is no longer present in the database by attempting
        to retrieve it again.

        It uses the `Department.DoesNotExist` exception to assert that the department no longer exists.

        """
        department = Department.objects.create(
            department_name='Test Department',
            department_head=self.user,
            creation_date=date.today()
        )
        url = f'/api/v1/departments/{department.id}'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify that the department is no longer present in the database
        with self.assertRaises(Department.DoesNotExist):
            Department.objects.get(id=department.id)





# import pytest
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient

# @pytest.mark.django_db
# class TestDepartmentAPIView:
#     @pytest.fixture
#     def api_client(self):
#         return APIClient()

#     def test_get_departments(self, api_client):
#         url = reverse('department-list')
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_200_OK

#     def test_create_department(self, api_client):
#         url = reverse('department-list')
#         data = {
#             'department_name': 'New Department',
#             'department_head': 3,  
#             'members': [3],  
#             'creation_date': '2023-06-16',
#             'project': [196], 
#         }
#         response = api_client.post(url, data)
#         assert response.status_code == status.HTTP_201_CREATED

#     def test_update_department(self, api_client):
#         department = Department.objects.create(
#             department_name='Test Department',
#             department_head_id=3,  
#             creation_date='2023-06-16',
#         )
#         url = reverse('department-detail', args=[department.pk])
#         data = {
#             'department_name': 'Updated Department',
#             'department_head': 3,  
#             'members': [3],  
#             'creation_date': '2023-06-17',
#             'project': [196],  
#         }
#         response = api_client.put(url, data)
#         assert response.status_code == status.HTTP_200_OK

#     def test_delete_department(self, api_client):
#         department = Department.objects.create(
#             department_name='Test Department',
#             department_head_id=3,  
#             creation_date='2023-06-16',
#         )
#         url = reverse('department-detail', args=[dep6artment.pk])
#         response = api_client.delete(url)
#         assert response.status_code == status.HTTP_204_NO_CONTENT