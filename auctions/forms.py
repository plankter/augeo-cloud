import floppyforms as forms

from .models import Auction, Bid


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ('start', 'end', 'active',)
        widgets = {
            'start': forms.DateTimeInput(attrs={'placeholder': 'Date & Time'}),
            'end': forms.DateTimeInput(attrs={'placeholder': 'Date & Time'}),
            'active': forms.CheckboxInput,
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('amount',)