from django.shortcuts import render

from auctions.models import Auction, Bet
from core.models import CustomUser
from products.models import Product


# Create your templates here.
def home(request):
    products = Product.objects.all().count()
    auctions = Auction.objects.all().count()
    users = CustomUser.objects.all().count()

    highest_bet = Bet.objects.all().earliest("-bet_amount")
    return render(request, 'core/home.html',
                  {'products': products, "auctions": auctions, "users": users, "highest_bet": highest_bet})
