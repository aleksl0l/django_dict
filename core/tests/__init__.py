from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from core.models import User


class TestFactory(APITestCase):
    def setUp(self):
        self.test_username = 'TestUsername'
        self.test_password = 'StrongPassword'
        self.user = self.create_user()

    def create_user(self):
        user = User.objects.create_user(username=self.test_username, password=self.test_password)
        return user


class RequestMixin:
    _headers = None

    def create_user_request(self, payload: dict) -> Response:
        url = reverse('users-list')
        return self.client.post(url, payload, format='json')
    
    def login_request(self, payload: dict) -> Response:
        url = reverse('user_login')
        return self.client.post(url, payload, format='json')

    def create_set_request(self, payload: dict) -> Response:
        url = reverse('sets-list')
        return self.client.post(url, payload, format='json', **self.headers)

    def get_set_list_request(self) -> Response:
        url = reverse('sets-list')
        return self.client.get(url, **self.headers)

    @property
    def headers(self):
        if not self._headers:
            payload = {'username': self.test_username, 'password': self.test_password}
            token = self.login_request(payload).data.get('token')
            self._headers = {'HTTP_AUTHORIZATION': f'Token {token}'}
        return self._headers
