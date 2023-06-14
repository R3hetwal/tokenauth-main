import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.skip
def test_login():
    print("Login Successful !!!")

@pytest.mark.mul
def testCalculation():
    assert 2*3 == 6

@pytest.mark.regression
def testLogoff():
    print("Logging out successfully!!!")


##################################  LOGIN TEST  ####################################################
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from users.models import User


class LoginTestCase(APITestCase):
    def setUp(self):
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
        # Send a POST request to the login endpoint
        data = {
            'email': self.email,
            'password': self.password
        }
        response = self.client.post('/users/v1/login/', data)

        # Check the response status code and token key
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], self.token)


