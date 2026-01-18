from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UsersTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', email='admin@example.com', password='admin123', role='admin')
        self.manager = User.objects.create_user(username='manager', email='manager@example.com', password='manager123', role='manager')
        self.staff = User.objects.create_user(username='staff', email='staff@example.com', password='staff123', role='staff')

        self.client = APIClient()

    def test_admin_can_create_user(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/users/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'pass1234',
            'role': 'staff'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_manager_cannot_create_user(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.post('/api/users/', {
            'username': 'otheruser',
            'email': 'other@example.com',
            'password': 'pass1234',
            'role': 'staff'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_cannot_create_user(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.post('/api/users/', {
            'username': 'user3',
            'email': 'user3@example.com',
            'password': 'pass1234',
            'role': 'manager'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_user_role(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(f'/api/users/{self.staff.id}/', {
            'username': 'staff',
            'email': 'staff@example.com',
            'role': 'manager'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], 'manager')

    def test_staff_cannot_update_user(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.put(f'/api/users/{self.manager.id}/', {
            'username': 'manager',
            'email': 'manager@example.com',
            'role': 'staff'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
