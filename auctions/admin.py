from django.contrib import admin

from auctions.models import Auction, Bet


# Register your models here.
@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('item', 'start_date', 'end_date','currency', 'base_price')
    ordering = ('base_price', 'item')
    search_fields = ('item', 'base_price')
    date_hierarchy = 'end_date'

@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ('user', 'auction', 'bet_amount')
    ordering = ('bet_amount',)
    search_fields = ('user',)

