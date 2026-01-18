from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from menu.models import Category, Product

User = get_user_model()

class MenuTests(TestCase):
    def setUp(self):
        # Users
        self.admin = User.objects.create_user(username='admin', email='admin@example.com', password='admin123', role='admin')
        self.staff = User.objects.create_user(username='staff', email='staff@example.com', password='staff123', role='staff')

        self.client = APIClient()

        # Category
        self.category = Category.objects.create(name='Pizza')

    def test_admin_can_create_product(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            '/api/menu/products/',
            {
                'name': 'Margherita',
                'category_id': self.category.id,
                'price': "10.00",
                'is_available': True,
                'preparation_time': 10
            },
            format='json'
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_staff_cannot_create_product(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.post(
            '/api/menu/products/',
            {
                'name': 'Pepperoni',
                'category_id': self.category.id,
                'price': "12.00",
                'is_available': True,
                'preparation_time': 12
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_get_products(self):
        Product.objects.create(name='Cheese', category=self.category, price=8.0)
        self.client.force_authenticate(user=self.staff)
        response = self.client.get('/api/menu/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) >= 1)
