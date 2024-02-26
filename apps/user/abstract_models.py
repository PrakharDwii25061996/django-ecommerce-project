
from django.db import models
import uuid


class BaseModel(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False)
    uuid = models.UUIDField(editable=False, default=uuid.uuid4)
    created_at = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    class Meta:
        abstract = True
