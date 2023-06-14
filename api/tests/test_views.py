from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .factories import AccountFactory, AccountDataTypeFactory


class APIViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.data = {"bbox": "37.51,55.67~37.65,55.63", "limit": 5}
        self.account = AccountFactory()
        self.account.create_token()
        self.account.data_type.set([AccountDataTypeFactory(slug="cars")])
        self.account.save()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.account.token)

    def get_response(self):
        return self.client.post(reverse("api:cars"), data=self.data, format='json')

    def test_no_token_access(self):
        self.client.credentials()
        response = self.get_response()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_with_token_and_permissions(self):
        response = self.get_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_without_data_type(self):
        self.account.data_type.set([])
        response = self.get_response()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertJSONEqual(
            response.content.decode("utf-8"),
            {"detail": "This data type is not available for your account"},
        )

    def test_request_day_limit_exceed(self):
        self.account.request_day_count = self.account.request_day_limit + 1
        self.account.save()

        response = self.get_response()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertJSONEqual(
            response.content.decode("utf-8"),
            {"detail": "Your request limit has been exceeded"},
        )

    def test_request_month_limit_exceed(self):
        self.account.request_month_count = self.account.request_month_limit + 1
        self.account.save()

        response = self.get_response()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertJSONEqual(
            response.content.decode("utf-8"),
            {"detail": "Your request limit has been exceeded"},
        )

    def test_request_total_limit_exceed(self):
        self.account.request_total_count = self.account.request_total_limit + 1
        self.account.save()

        response = self.get_response()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertJSONEqual(
            response.content.decode("utf-8"),
            {"detail": "Your request limit has been exceeded"},
        )

    def test_expired(self):
        self.account.active = False
        self.account.save()

        response = self.get_response()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertJSONEqual(
            response.content.decode("utf-8"),
            {"detail": "Your account has been expired"},
        )

    def test_not_enough_data(self):
        self.data = {"func": "avg", "size": 100}

        response = self.get_response()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(
            response.content.decode("utf-8"),
            {"detail": "Please pass coordinates"},
        )

