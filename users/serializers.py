from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'read_only': True},
            'is_superuser': {'read_only': True},
        }

    def validate_email(self, value):
        user_id = self.instance.id if self.instance else None
        if User.objects.exclude(id=user_id).filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_role(self, value):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if value == User.Role.ADMIN and (not user or user.role != User.Role.ADMIN):
            raise PermissionDenied("Only admin can assign admin role")
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        role = validated_data.pop('role', None)
        user = getattr(self.context.get('request'), 'user', None)

        if role is not None:
            if not user or user.role != User.Role.ADMIN:
                raise PermissionDenied("You cannot change user role")
            if isinstance(role, str):
                role = getattr(User.Role, role.upper(), role)
            instance.role = role

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def create(self, validated_data):
        user = getattr(self.context.get('request'), 'user', None)

        if 'role' in validated_data:
            if isinstance(validated_data['role'], str):
                validated_data['role'] = getattr(User.Role, validated_data['role'].upper())
            if not user or user.role != User.Role.ADMIN:
                validated_data['role'] = User.Role.STAFF
        else:
            validated_data['role'] = User.Role.STAFF

        password = validated_data.pop('password', None)
        user_obj = User(**validated_data)
        if password:
            user_obj.set_password(password)
        user_obj.save()
        return user_obj

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = getattr(self.context.get('request'), 'user', None)
        if user and user.role != User.Role.ADMIN:
            data.pop('role', None)
        return data
