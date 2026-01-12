from rest_framework import serializers
from .models import Order, OrderItem
from customers.models import Customer
from menu.serializers import ProductSerializer
from menu.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price', 'subtotal']
        read_only_fields = ['price', 'subtotal']

    def validate_product_id(self, value):
        if not value.is_available:
            raise serializers.ValidationError(f"{value.name} is not available.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        write_only=True
    )

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_id','order_date', 'total_amount','status', 'notes', 'items']
        read_only_fields = ['order_date', 'total_amount', 'status']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        customer = validated_data.pop('customer_id')

        order = Order.objects.create(customer=customer)

        for item_data in items_data:
            product = item_data['product_id']
            quantity = item_data['quantity']

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price 
            )

        return order
    
    def validate(self, data):
        if not data.get('items'):
            raise serializers.ValidationError("Order must contain at least one item.")
        return data

