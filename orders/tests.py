from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from menu.models import Product, Category
from customers.models import Customer
from .models import Order, OrderItem
from decimal import Decimal
User = get_user_model()

class OrdersTests(TestCase):
    def setUp(self):
        # Users
        self.admin = User.objects.create_user(username='admin', email='admin@example.com', password='admin123', role='admin')
        self.manager = User.objects.create_user(username='manager', email='manager@example.com', password='manager123', role='manager')
        self.staff = User.objects.create_user(username='staff', email='staff@example.com', password='staff123', role='staff')
        self.client = APIClient()

        # Category & Products
        self.cat = Category.objects.create(name="Pizza")
        self.prod1 = Product.objects.create(name="Margherita", category=self.cat, price=10.0, is_available=True, preparation_time=10)
        self.prod2 = Product.objects.create(name="Pepperoni", category=self.cat, price=12.0, is_available=True, preparation_time=12)

        # Customer
        self.customer = Customer.objects.create(first_name="John", last_name="Doe", email="john@example.com", phone="+123456789", address="Street 1")

        # Existing order
        self.order = Order.objects.create(customer=self.customer)
        self.order_item = OrderItem.objects.create(order=self.order, product=self.prod1, quantity=2, price=self.prod1.price, subtotal=2*self.prod1.price)
        self.order.update_total_amount()

    def test_admin_can_create_order(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/orders/orders/', {
            "customer_id": self.customer.id,
            "items": [
                {"product_id": self.prod1.id, "quantity": 1},
                {"product_id": self.prod2.id, "quantity": 2}
            ]
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Decimal(response.data['total_amount']), self.prod1.price*1 + self.prod2.price*2)

    def test_staff_cannot_create_order(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.post('/api/orders/orders/', {
            "customer_id": self.customer.id,
            "items": [{"product_id": self.prod1.id, "quantity": 1}]
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_get_orders(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.get('/api/orders/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_order_status_valid(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.put(f'/api/orders/orders/{self.order.id}/update_status/', {"status": "Preparing"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "Preparing")

    def test_update_order_status_invalid_transition(self):
        self.client.force_authenticate(user=self.manager)
        # Trying to go from New -> Ready (skipping Preparing)
        response = self.client.put(f'/api/orders/orders/{self.order.id}/update_status/', {"status": "Ready"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
