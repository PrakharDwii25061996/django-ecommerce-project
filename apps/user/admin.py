from django.contrib import admin
from .models import CustomUser

# admin.site.unregister(Group)

admin.site.register(CustomUser)