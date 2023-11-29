from django.contrib.auth.models import User
from django.db import models

from core.models import CustomUser


# Create your models here.
class Event(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="User")
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(verbose_name="Description")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated")
    start_date = models.DateTimeField()

    def __str__(self):
        return f"Event: {self.name}"
