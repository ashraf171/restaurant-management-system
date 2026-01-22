from rest_framework import serializers
from .models import Order, OrderItem
from customers.models import Customer
from menu.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price', 'subtotal']
        read_only_fields = ['price', 'subtotal']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value

    def validate_product_id(self, value):
        if not value.is_available:
            raise serializers.ValidationError(f"{value.name} is not available for order")
        return value

    def create(self, validated_data):
        product = validated_data.pop('product_id')
        validated_data['product'] = product
        validated_data['price'] = product.price
        item = OrderItem.objects.create(**validated_data)
        return item


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), write_only=True
    )

    class Meta:
        model = Order
        fields = ['id', 'customer_id', 'order_date', 'total_amount', 'status', 'notes', 'items']
        read_only_fields = ['order_date', 'total_amount', 'status']

    def validate_items(self, value):
        product_ids = [item['product_id'].id for item in value]
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError("Duplicate products in the order are not allowed")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        customer = validated_data.pop('customer_id')
        order = Order.objects.create(customer=customer)

        for item_data in items_data:
            product = item_data.pop('product_id')
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price=product.price,
                subtotal=product.price * item_data['quantity']
            )
        order.update_total_amount()
        return order
