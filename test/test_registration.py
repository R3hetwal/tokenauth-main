
from django.test import RequestFactory
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from users.models import User

"""
    Unit test case for the user registration functionality.

    This test case verifies the behavior of the user registration endpoint by testing the registration 
    process using POST requests with valid and invalid data.

    Attributes:
        client (APIClient): An instance of the APIClient for making test requests.
        factory (RequestFactory): An instance of the RequestFactory for creating mock requests.

    Methods:
        setUp(): Set up the necessary objects and credentials for testing.
        test_user_registration(): Test the user registration functionality by making a POST request to 
                                  the registration endpoint with valid data and checking the response.
        test_user_registration_invalid_data(): Test the user registration endpoint behavior when invalid 
                                               data is provided by making a POST request with invalid data 
                                               and checking the response.

"""


class UserRegistrationViewSetTest(APITestCase):
    def setUp(self):
        """
        Set up the necessary objects and credentials for testing.

        This method initializes the APIClient for making test API requests and the RequestFactory for 
        creating mock requests.

        It sets the `client` attribute as an instance of `APIClient` for making HTTP requests during the 
        tests.
        The `factory` attribute is set as an instance of `RequestFactory` for creating mock requests.

        """
        self.client = APIClient()
        self.factory = RequestFactory()

    def test_user_registration(self):
        """
        Test case for user registration.

        This test verifies the registration process for a new user by making a POST request to the registration 
        endpoint.

        It constructs the URL for the registration endpoint and prepares the data payload containing the necessary 
        user information.
        The data payload includes fields such as email, password, confirm_password, user_name, first_name, last_name, 
        and contact.

        It creates a mock POST request using the `RequestFactory` and sends the request using the `client.post` method.
        The response from the registration endpoint is captured and printed for debugging purposes.

        It asserts the expected status code of the response, which is `status.HTTP_200_OK`.
        It also verifies the presence of specific keys in the response data dictionary, such as 'status', 'payload', 
        'token', and 'msg'.

        """
        url = '/users/v1/sign-up/'  
        data = {
            'email':'test52@gmail.com',
            'user_name':'test52',
            'first_name':'testuser',
            'last_name':'test',
            'contact':'9813256040',
            'password':'Test1212*',
            'confirm_password':'Test1212*'
        }
        request = self.factory.post(url)
        response = self.client.post(url, data)
        # print(response)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertEqual(response.data['status'], 200)
        self.assertIn('payload', response.data)
        self.assertIn('token', response.data)
        self.assertIn('msg', response.data)

    def test_user_registration_invalid_data(self):
        """
        Test case for user registration with invalid data.

        This test verifies the behavior of the user registration endpoint when invalid data is provided.

        It constructs the URL for the registration endpoint and prepares the invalid data payload.
        The invalid data payload includes fields such as 'username', 'email', and 'password'.

        It sends a POST request to the registration endpoint using the `client.post` method with the 
        invalid data payload.
        The response from the registration endpoint is captured.

        It asserts the expected status code of the response, which is `status.HTTP_400_BAD_REQUEST`.
        This ensures that the registration endpoint properly handles the invalid data and returns an 
        appropriate error response.

        """
        url = '/users/v1/sign-up/'  
        invalid_data = {
            'username': '',  
            'email': 'test@example.com',
            'password': 'testpassword',
        }

        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

