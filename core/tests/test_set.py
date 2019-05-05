from rest_framework import status

from core.models import Set
from core.tests import TestFactory, RequestMixin
from core.tests.data_samples import set_create_json


class SetTestCase(TestFactory, RequestMixin):

    def test_set(self):
        response = self.create_set_request(set_create_json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Set.objects.last().name, set_create_json.get('name'))

        response_list = self.get_set_list_request()
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_list.data), 1)
