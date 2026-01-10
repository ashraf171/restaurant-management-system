from rest_framework import serializers 
from .models import Category,Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name','description','is_active','slug','created_at','updated_at']
        read_only_fields=['slug','created_at','updated_at']





class ProductSerializer(serializers.ModelSerializer):
    category=CategorySerializer(read_only=True)
    category_id=serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True
    )

    class Meta:
        model=Product
        fields=['id','category','category_id','name','description','price','is_available','preparation_time','created_at','updated_at']
        read_only_fields=['id','created_at','updated_at']

    def create(self, validated_data):
        category = validated_data.pop('category_id')
        product = Product.objects.create(
        category=category,
        **validated_data
        )
        return product
