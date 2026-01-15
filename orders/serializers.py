from rest_framework import serializers
from .models import Order, OrderItem
from customers.models import Customer
from menu.serializers import ProductSerializer
from menu.models import Product
from django.core.exceptions import ValidationError

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price', 'subtotal']
        read_only_fields = ['price', 'subtotal']

    def validate_product_id(self, value):
        if not value.is_available:
            raise serializers.ValidationError(f"{value.name} is not available.")
        return value

    def create(self, validated_data):
        product = validated_data['product_id']
        if not product.is_available:
            raise ValidationError(f"{product.name} is not available.")
        validated_data['price'] = product.price
        item = OrderItem.objects.create(**validated_data)
        product.is_available = False
        product.save(update_fields=['is_available'])
        item.order.update_total_amount()
        return item


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_id','order_date', 'total_amount','status', 'notes', 'items']
        read_only_fields = ['order_date', 'total_amount', 'status']

    def validate(self, data):
        if not data.get('items'):
            raise serializers.ValidationError("Order must contain at least one item.")
        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        customer = validated_data.pop('customer_id')
        order = Order.objects.create(customer=customer)
        for item_data in items_data:
            item_data['order'] = order
            serializer = OrderItemSerializer(data=item_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return order

    def update(self, instance, validated_data):
        if 'items' in validated_data:
            items_data = validated_data.pop('items')
            instance.items.all().delete()
            for item_data in items_data:
                item_data['order'] = instance
                serializer = OrderItemSerializer(data=item_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        return super().update(instance, validated_data)
