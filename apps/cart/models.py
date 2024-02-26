from django.db import models
from django.conf import settings

from apps.product.models import Product


class Cart(models.Model):
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE
	)
	items = models.ManyToManyField(
		Product,
		related_name='products',
	)
	number_of_item = models.IntegerField(default=0)
