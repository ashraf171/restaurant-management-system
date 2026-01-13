from rest_framework import serializers
from .models import User



class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.Role.choices, default=User.Role.STAFF)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role", "role_display"]
        read_only_fields = ["id"]
