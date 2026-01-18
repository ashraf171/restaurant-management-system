from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from customers.models import Customer

User = get_user_model()

class CustomersTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', email='admin@example.com', password='admin123', role='admin')
        self.manager = User.objects.create_user(username='manager', email='manager@example.com', password='manager123', role='manager')
        self.staff = User.objects.create_user(username='staff', email='staff@example.com', password='staff123', role='staff')
        self.client = APIClient()

        # Customers
        self.cust1 = Customer.objects.create(first_name='John', last_name='Doe', email='john@example.com', phone='+123456789', address='Street 1')

    def test_admin_can_create_customer(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/customers/customers/', {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com',
            'phone': '+987654321',
            'address': 'Street 2'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_staff_cannot_create_customer(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.post('/api/customers/customers/', {
            'first_name': 'Bob',
            'last_name': 'Brown',
            'email': 'bob@example.com',
            'phone': '+111222333',
            'address': 'Street 3'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_get_customers(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.get('/api/customers/customers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
