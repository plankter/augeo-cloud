import floppyforms as forms

from .models import Auction, Bid


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ('start', 'end',)
        widgets = {
            'start': forms.DateTimeInput(attrs={'placeholder': 'Date & Time'}),
            'end': forms.DateTimeInput(attrs={'placeholder': 'Date & Time'}),
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('amount',)