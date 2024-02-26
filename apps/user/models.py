from django.contrib.auth.models import (
	AbstractBaseUser, PermissionsMixin
)
from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from PIL import Image

from .abstract_models import BaseModel
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    mobile_number = models.CharField(max_length=55, null=False)
    permanent_address = models.CharField(max_length=55, null=False)
    residential_address = models.CharField(max_length=55, null=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    password = models.CharField(max_length=555, null=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='profile/user/', null=True)
    alternate_number = models.CharField(max_length=55, null=True)
    city = models.CharField(max_length=55, null=True)
    state = models.CharField(max_length=55, null=True)
    country = models.CharField(max_length=55, null=True)
    postal_code = models.CharField(
        max_length=6,
        validators=[RegexValidator('^[0-9]{6}$', _('Invalid postal code'))],
        null=True
    )
    latitude = models.CharField(max_length=100, null=True)
    longitude = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.user.email}'

    def save(self, *args, **kwargs):
        super().save()

        if self.image:
            image = Image.open(self.image.path)

            if (
                image.height > settings.PROFILE_IMAGE_HEIGHT
                or image.width > settings.PROFILE_IMAGE_WIDTH
            ):
                image_size = (
                    settings.PROFILE_IMAGE_HEIGHT,
                    settings.PROFILE_IMAGE_WIDTH,
                )
                image.thumbnail(image_size)
                image.save(self.image.path)
