from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'is_active', 'slug', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError()
        return value


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(is_active=True),
        write_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'category_id',
            'name',
            'description',
            'price',
            'is_available',
            'preparation_time',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError()
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError()
        return value

    def validate_preparation_time(self, value):
        if value < 0:
            raise serializers.ValidationError()
        return value

    def validate(self, attrs):
        category = attrs.get('category_id') or getattr(self.instance, 'category', None)
        name = attrs.get('name') or getattr(self.instance, 'name', None)
        if Product.objects.exclude(id=getattr(self.instance, 'id', None)).filter(
            category=category,
            name=name
        ).exists():
            raise serializers.ValidationError()
        return attrs

    def create(self, validated_data):
        category = validated_data.pop('category_id')
        return Product.objects.create(category=category, **validated_data)

    def update(self, instance, validated_data):
        if 'category_id' in validated_data:
            instance.category = validated_data.pop('category_id')
        return super().update(instance, validated_data)
