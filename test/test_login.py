from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from users.models import User

"""
    Unit test case for the login functionality.

    This test case verifies the behavior of the login endpoint by testing the login process using a POST
    request.

    Attributes:
        client (APIClient): An instance of the APIClient for making test requests.
        email (str): The email address of the test user.
        password (str): The password of the test user.
        user_name (str): The username of the test user.
        first_name (str): The first name of the test user.
        token (str): The token associated with the test user.

    Methods:
        setUp(): Set up the necessary objects and credentials for testing.
        test_login(): Test the login functionality by sending a POST request to the login endpoint and 
                      checking the response.

"""

class LoginTestCase(APITestCase):
    def setUp(self):
        """
        Set up the necessary objects and credentials for testing.

        This method initializes the APIClient for making test API requests.
        It also sets up various attributes such as email, password, user_name, first_name, and token.

        The method creates a user with the specified email, password, user_name, and first_name using the User model's
        `create_user` method. Additional fields can be added if required.

        It generates a token for the user using the Token model's `create` method.
        
        """
        self.client = APIClient()
        self.email = 'detective@gmail.com'
        self.password = 'Sherlock1212*'
        self.user_name = 'thedetctive',
        self.first_name = 'Shelly',
        self.token = '930222e0e90e46fec7bc21f6d32b9db5daea3046'

        # Create a user and generate a token
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password,
            user_name=self.user_name,
            first_name=self.first_name
            # Add any other required fields
        )
        Token.objects.create(user=self.user, key=self.token)

    def test_login(self):
        """
        Test the login functionality by sending a POST request to the login endpoint.

        This method sends a POST request to the '/users/v1/login/' URL using the test client.
        It includes the user's email and password in the request data.

        The method asserts that the response status code is HTTP 200 OK, indicating a successful login.
        It also verifies that the response data contains the expected token key.

        """
        data = {
            'email': self.email,
            'password': self.password
        }
        response = self.client.post('/users/v1/login/', data)

        # Check the response status code and token key
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], self.token)


