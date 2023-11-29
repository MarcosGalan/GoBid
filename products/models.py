from django.db import models
from django.forms import CharField

from core.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=10, verbose_name="Category")

    def __str__(self):
        return self.name


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="Name")
    subtitle = models.CharField(max_length=255, verbose_name="Subtitle")
    description = models.TextField(verbose_name="Description")
    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(verbose_name="Image", blank=True, null=True, upload_to='products')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated")

    def __str__(self):
        return self.title


class Item(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Owner")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(verbose_name="Image", blank=True, null=True, upload_to='items')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated")

    def __str__(self):
        return f"{self.name}"
