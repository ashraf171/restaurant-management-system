from rest_framework import serializers

from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta :
        model = Customer
        fields = ['id','first_name','last_name','email','phone','address','registration_date']
        read_only_fields=['registration_date']


