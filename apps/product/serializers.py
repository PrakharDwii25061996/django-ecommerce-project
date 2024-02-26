from rest_framework import serializers
from .models import Product, Category, SubCategory


class CategorySerializer(serializers.ModelSerializer):

	class Meta:
		model = Category
		fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):

	class Meta:
		model = SubCategory
		fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
	image = serializers.ImageField(allow_null=True)

	class Meta:
		model = Product
		fields = '__all__'


class TokenSerializer(serializers.Serializer):
	token = serializers.CharField(max_length=555)


class PaymentSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=555)
	price = serializers.IntegerField()
