from django.forms import ModelForm

from .models import Auction, Bid


class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        exclude = ('lot',)


class BidForm(ModelForm):
    class Meta:
        model = Bid