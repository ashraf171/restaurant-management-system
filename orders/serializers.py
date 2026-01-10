from rest_framework import serializers
from .models import Order, OrderItem
#from customers.serializers import CustomerSerializer
from customers.models import Customer
from menu.serializers import ProductSerializer
from menu.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)
    price = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price', 'subtotal']

    def get_price(self, obj):
        return obj.product.price

    def get_subtotal(self, obj):
        return obj.quantity * obj.product.price

    def validate_product_id(self, value):
        if not value.is_available:
            raise serializers.ValidationError(f"{value.name} is not available.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    #customer = CustomerSerializer(read_only=True)
    #customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), write_only=True)
    items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_id', 'order_date', 'total_amount', 'status', 'notes', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        customer = validated_data.pop('customer_id')
        order = Order.objects.create(customer=customer, **validated_data)

        for item_data in items_data:
            product = item_data['product_id']
            quantity = item_data['quantity']
            OrderItem.objects.create(order=order, product=product, quantity=quantity)

        
        return order
