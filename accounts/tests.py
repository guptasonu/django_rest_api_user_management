from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts import models as account_models


class UserRegisterTestCase(APITestCase):
    def test_registration(self):
        payload = {
            "username": "gsonu@gmail.com",
            "password": "sonu@12345",
            "first_name": "test sonu",
            "last_name": "test gupta",
            "notes": "third user",
        }
        response = self.client.post(reverse("UserRegister"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserTestCase(APITestCase):
    def setUp(self):
        self.user = account_models.User.objects.create_user(
            username="gsonu@gmail.com", password="password", email="gsonu@gmail.com"
        )
        self.token = account_models.Token.objects.create(user=self.user)
        self.api_authenticaion()

    def api_authenticaion(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_user_list(self):
        response = self.client.get(reverse("ListUser"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]["email"], "gsonu@gmail.com")

    def test_user_update(self):
        payload = {"first_name": "Sonu"}
        response = self.client.put(
            reverse("UpdateUser", kwargs={"pk": self.user.id}), payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("first_name"), "Sonu")

    def test_user_delete(self):
        response = self.client.delete(
            reverse("DeleteUser", kwargs={"pk": self.user.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
