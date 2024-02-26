from rest_framework import serializers

from .models import Cart


class CartAddProductSerializer(serializers.ModelSerializer):
	user = serializers.IntegerField()
	product_id = serializers.IntegerField()
	
	class Meta:
		model = Cart
		fields = ['user', 'product_id']


class CartRemoveProductSerializer(serializers.ModelSerializer):
	user = serializers.IntegerField()
	product_id = serializers.IntegerField()

	class Meta:
		model = Cart
		fields = ['user', 'product_id']
