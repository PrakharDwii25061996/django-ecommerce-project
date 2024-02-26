""" product/models.py """
from django.db import models
# 

class Category(models.Model):
	name = models.CharField(max_length=55)


class SubCategory(models.Model):
	name = models.CharField(max_length=55)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)


class ProductImage(models.Model):
	image = models.ImageField(upload_to='product/', null=True)


class Product(models.Model):
	name = models.CharField(max_length=55)
	detail = models.CharField(max_length=500, null=True)
	image = models.ImageField(upload_to='images/product/', null=True)
	associative_image = models.ForeignKey(ProductImage, on_delete=models.CASCADE, null=True)
	subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
	brand = models.CharField(max_length=55)
	price = models.DecimalField(decimal_places=2, max_digits=10, null=False)
	quantity = models.IntegerField(default=1, null=True)
	color = models.CharField(max_length=100, null=False)
	featured = models.BooleanField(default=False)
	currency = models.CharField(max_length=55)
	discount = models.IntegerField(default=0)
	average_rating = models.IntegerField(default=0, null=True)
	number_of_rating = models.IntegerField(default=0, null=True)
	number_of_likes = models.IntegerField(default=0, null=True)
