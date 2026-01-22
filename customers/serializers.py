from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'phone', 'address', 'registration_date']
        read_only_fields = ['full_name', 'registration_date']

    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("First name cannot be empty")
        return value

    def validate_last_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Last name cannot be empty")
        return value

    def validate_phone(self, value):

        return value

    def validate_address(self, value):
        if len(value) > 500:
            raise serializers.ValidationError("Address too long")
        return value
