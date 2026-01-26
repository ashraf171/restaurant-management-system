from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Category, Product

User = get_user_model()

class MenuTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin', email='admin@example.com', password='admin123', role=User.Role.ADMIN
        )
        self.manager = User.objects.create_user(
            username='manager', email='manager@example.com', password='manager123', role=User.Role.MANAGER
        )
        self.staff = User.objects.create_user(
            username='staff', email='staff@example.com', password='staff123', role=User.Role.STAFF
        )

        self.category = Category.objects.create(name="Drinks")
        self.product_available = Product.objects.create(
            name="Coke", category=self.category, price=1.5, is_available=True
        )
        self.product_unavailable = Product.objects.create(
            name="Fanta", category=self.category, price=1.3, is_available=False
        )

        self.client = APIClient()

    def test_admin_can_create_category(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/categories/', {'name': 'Food'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Food')

    def test_staff_cannot_create_category(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.post('/api/categories/', {'name': 'Food'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_product(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/products/', {
            'name': 'Pepsi',
            'category_id': self.category.id,
            'price': 2.0,
            'is_available': True
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Pepsi')

    def test_staff_can_get_only_available_products(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        results = data['results']
        self.assertIsInstance(results, list)

        for p in results:
            self.assertTrue(p['is_available'])

    def test_manager_can_update_product(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.put(f'/api/products/{self.product_available.id}/', {
            'name': 'Coke Zero',
            'category_id': self.category.id,
            'price': 1.8,
            'is_available': True
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Coke Zero')
