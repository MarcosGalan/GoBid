"""
URL configuration for GoBid project.

The `urlpatterns` list routes URLs to templates. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function templates
    1. Add an import:  from my_app import templates
    2. Add a URL to urlpatterns:  path('', templates.home, name='home')
Class-based templates
    1. Add an import:  from other_app.templates import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from auctions.views import AuctionDetailView, AuctionsListView, UserAuctions,AuctionUpdateView,AuctionCreateView
from auctions.views import AuctionDetailView, AuctionsListView, GetBetById, GetBetsByAuctionId

urlpatterns = [
    path('auction/<int:pk>/', AuctionDetailView.as_view(), name="auction"),
    path('auctions/', AuctionsListView.as_view(), name="auctions"),
    path('fetch/bet/<int:bet_id>/', GetBetById, name='GetBetById'),
    path('fetch/auction/<int:auction_id>/', GetBetsByAuctionId, name='GetBetsByAuctionId'),
    path('user/auctions/', UserAuctions.as_view(), name="user-auctions"),
    path('user/auction/<int:pk>/', AuctionUpdateView.as_view(), name="user-auction-update"),
    path('user/auction/', AuctionCreateView.as_view(), name="user-auction-create"),


]
