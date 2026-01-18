from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }

    def update(self, instance, validated_data):

        role = validated_data.get('role')
        if role in [choice[0] for choice in User.Role.choices]:
            instance.role = role
        validated_data.pop('role', None)


        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
