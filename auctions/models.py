from django.db import models
from django.contrib.auth.models import User

from core.models import CustomUser
from products.models import Item


# Create your models here.
class Auction(models.Model):
    item = models.ForeignKey(Item, verbose_name="Item", on_delete=models.CASCADE)
    start_date = models.DateTimeField(verbose_name="Start Date")
    end_date = models.DateTimeField(verbose_name="End Date")
    base_price = models.IntegerField(verbose_name="Base Price")
    currency = models.CharField(max_length=10, verbose_name="Currency")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    updated = models.DateTimeField(auto_now=True, verbose_name="Last Update")


class Bet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, verbose_name="User")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, verbose_name="Auction")
    bet_amount = models.IntegerField(verbose_name="Bet Amount")
