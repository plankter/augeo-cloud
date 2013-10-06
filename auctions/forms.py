from django.forms import ModelForm, DateTimeInput

from .models import Auction, Bid


class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ('start', 'end', 'active',)


class BidForm(ModelForm):
    class Meta:
        model = Bid