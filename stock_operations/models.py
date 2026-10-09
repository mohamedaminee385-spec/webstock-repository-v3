from django.db import models
import uuid
# Create your models here
class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    stock_number = models.IntegerField(default=0)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name