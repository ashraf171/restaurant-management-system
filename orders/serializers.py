from rest_framework import serializers
from .models import Order, OrderItem
from customers.models import Customer
from menu.serializers import ProductSerializer
from menu.models import Product
from django.core.exceptions import ValidationError

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price', 'subtotal']
        read_only_fields = ['price', 'subtotal']

    def create(self, validated_data):
        product = validated_data.pop('product_id')
        validated_data['product'] = product
        validated_data['price'] = product.price
        item = OrderItem.objects.create(**validated_data)
        return item


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_id', 'order_date', 'total_amount', 'status', 'notes', 'items']
        read_only_fields = ['order_date', 'total_amount', 'status']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        customer = validated_data.pop('customer_id')
        order = Order.objects.create(customer=customer)


        for item_data in items_data:
            product = item_data.pop('product_id')
            item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price=product.price,
                subtotal=product.price * item_data['quantity']
            )
        order.update_total_amount()
        return order
