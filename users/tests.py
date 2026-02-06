from django.test import TestCase

from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTests(APITestCase):

    def test_register(self):
        data = {
            "username": "jorge",
            "email": "jorge@example.com",
            "password": "StrongPass123",
            "role": "user"
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        User.objects.create_user(username="jorge", email="jorge@example.com", password="StrongPass123")
        data = {"username": "jorge", "password": "StrongPass123"}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

