from django_restframework import serializers

from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta :
        model = Customer
        field = "__all__"


