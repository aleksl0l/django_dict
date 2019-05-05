from rest_framework import status

from core.tests import TestFactory, RequestMixin
from core.tests.data_samples import user_create_json


class UserTestCase(TestFactory, RequestMixin):

    def test_create_user(self):
        response = self.create_user_request(user_create_json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_login = self.login_request(user_create_json)
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)
        self.assertIn('token', response_login.data)
