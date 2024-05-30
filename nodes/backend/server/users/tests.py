from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import path, include, reverse
from django.contrib.auth.models import User
from rest_framework.request import Request
from django.test.client import RequestFactory
# Create your tests here.

class UsersTests(APITestCase):
    url_patterns = [
        path('', include('users.urls'))
    ]

    def setUp(self):
        self.loginUrl = reverse('users:login')
        self.logoutUrl = reverse('users:logout')
        self.registerUrl = reverse('users:register')


    def test_register_user_valid_status_code(self):
        body = {
            'username': 'johntest',
            'first_name': 'John',
            'last_name': 'Test',
            'email': 'johntest@wp.pl',
            'password': 'pas123',
            'password2': 'pas123'
        }
        resp = self.client.post(self.registerUrl, body)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        

    def test_register_user_valid_resp_body(self):
        body = {
            'username': 'johntest',
            'first_name': 'John',
            'last_name': 'Test',
            'email': 'johntest@wp.pl',
            'password': 'pas123',
            'password2': 'pas123'
        }
        resp = self.client.post(self.registerUrl, body)
        resp_body = resp.json()

        user = User.objects.get(username = resp_body['user']['username'])
        token = Token.objects.get(user = user).key
    
        del body['password']
        del body['password2']
        self.assertEqual(resp_body.get('user'), body)
        self.assertEqual(resp_body.get('token'), token)
        self.assertEqual(resp_body.get('success'), True)

    
    def test_register_password_match(self):
        body = {
            'username': 'johntest',
            'first_name': 'John',
            'last_name': 'Test',
            'email': 'johntest@wp.pl',
            'password': 'pas123',
            'password2': 'pas1234'
        }

        resp = self.client.post(self.registerUrl, body)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_email_unique(self):
        first_body = {
            'username': 'johntest',
            'first_name': 'John',
            'last_name': 'Test',
            'email': 'johntest@wp.pl',
            'password': 'pas123',
            'password2': 'pas123'
        }

        second_body = {
            'username': 'janetest',
            'first_name': 'Jane',
            'last_name': 'Test',
            'email': 'johntest@wp.pl',
            'password': 'pas123',
            'password2': 'pas123'
        }

        self.client.post(self.registerUrl, first_body)
        resp = self.client.post(self.registerUrl, second_body)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_valid_status_code(self):
        register_body = {
            'username': 'johntest',
            'first_name': 'John',
            'last_name': 'Test',
            'email': 'johntest@wp.pl',
            'password': 'pas123',
            'password2': 'pas123'
        }

        self.client.post(self.registerUrl, register_body)

        login_body = {
            'username': 'johntest',
            'password': 'pas123'
        }

        resp = self.client.post(self.loginUrl, login_body)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


    def test_login_valid_resp_body(self):
        register_body = {
            'username': 'johntest',
            'first_name': 'John',
            'last_name': 'Test',
            'email': 'johntest@wp.pl',
            'password': 'pas123',
            'password2': 'pas123'
        }

        resp = self.client.post(self.registerUrl, register_body)

        login_body = {
            'username': 'johntest',
            'password': 'pas123'
        }

        resp = self.client.post(self.loginUrl, login_body)
        resp_body = resp.json()

        user = User.objects.get(username=login_body['username'])
        token = Token.objects.get(user=user).key
    
        self.assertEqual(resp_body['username'], user.username)
        self.assertEqual(resp_body['token'], token)


    def test_login_user_not_exist(self):
        login_body = {
            'username': 'johntest',
            'password': 'pas123'
        }

        resp = self.client.post(self.loginUrl, login_body)
    
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_invalid_password(self):
        register_body = {
            'username': 'johntest',
            'first_name': 'John',
            'last_name': 'Test',
            'email': 'johntest@wp.pl',
            'password': 'pas123',
            'password2': 'pas123'
        }

        self.client.post(self.registerUrl, register_body)

        login_body = {
            'username': 'johntest',
            'password': 'pas1234'
        }

        resp = self.client.post(self.loginUrl, login_body)
        
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_valid(self):
        register_body = {
            'username': 'johntest',
            'first_name': 'John',
            'last_name': 'Test',
            'email': 'johntest@wp.pl',
            'password': 'pas123',
            'password2': 'pas123'
        }
        self.client.post(self.registerUrl, register_body)

        login_body = {
            'username': 'johntest',
            'password': 'pas123'
        }

        login_response = self.client.post(self.loginUrl, login_body)
        token = login_response.json().get('token')

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        resp = self.client.post(self.logoutUrl)


        self.assertEqual(resp.status_code, status.HTTP_200_OK)
    

    def test_logout_unauthorized(self):
        resp = self.client.post(self.logoutUrl)

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    
        
    
    
