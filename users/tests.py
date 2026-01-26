from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UsersTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role=User.Role.ADMIN
        )
        self.manager = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='manager123',
            role=User.Role.MANAGER
        )
        self.staff = User.objects.create_user(
            username='staff',
            email='staff@example.com',
            password='staff123',
            role=User.Role.STAFF
        )

        self.client = APIClient()

    def test_admin_can_create_user(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/users/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'pass1234',
            'role': User.Role.STAFF
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['role'], User.Role.STAFF)

    def test_admin_can_update_user_role(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            f'/api/users/{self.staff.id}/',
            {
                'role': User.Role.MANAGER
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], User.Role.MANAGER)

    def test_admin_can_delete_user(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f'/api/users/{self.staff.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.staff.id).exists())

    def test_cannot_delete_last_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f'/api/users/{self.admin.id}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(User.objects.filter(id=self.admin.id).exists())

    def test_non_admin_cannot_change_role(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.patch(
            f'/api/users/{self.staff.id}/',
            {
                'role': User.Role.MANAGER
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
