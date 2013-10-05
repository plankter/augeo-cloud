from django.contrib import admin

from .models import Auction, BidBasket, Bid


admin.site.register(Auction)
admin.site.register(BidBasket)
admin.site.register(Bid)