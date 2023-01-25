from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.test import APIClient

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


REGISTER_URL = reverse('user:create')
LOGIN_URL = reverse('user:login')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicAPITest(TestCase):
    '''public user api 테스트'''

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        '''회원가입 테스트'''
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
        }

        res = self.client.post(REGISTER_URL, payload)

        user = get_user_model().objects.get(email=payload['email'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_password_too_short_error(self):
        '''짧은 비밀번호 입력 시 에러 '''
        payload = {
            'email': 'test@gmail.com',
            'password': 'pw',
            'name': 'test name',
        }
        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_login(self):
        '''로그인 테스트'''
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
        }
        get_user_model().objects.create_user(**payload)

        res = self.client.post(LOGIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)

    def test_create_token_invalid_credentials(self):
        '''잘못된 비밀번호 입력 시 토큰 미생성'''
        payload1 = {
            'email': 'test@gmail.com',
            'password': 'testpass',
        }
        get_user_model().objects.create_user(**payload1)

        payload2 = {
            'email': 'test@gmail.com',
            'password': 'wrong',
        }

        res = self.client.post(LOGIN_URL, payload2)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('access', res.data)
