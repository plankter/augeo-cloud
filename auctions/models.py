from decimal import Decimal
from datetime import time
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User

from djmoney.models.fields import MoneyField

from core.models import Artwork
from .utils import get_current_time


class Auction(models.Model):
    ENGLISH_AUCTION = 'EA'
    FIRST_PRICE_SEALED_BID_AUCTION = 'FPSBA'

    AUCTION_TYPES = (
        (ENGLISH_AUCTION, 'English auction'),
        (FIRST_PRICE_SEALED_BID_AUCTION, 'First-price sealed-bid auction'),
    )

    lot = models.OneToOneField(Artwork, verbose_name="Lot", blank=False, db_index=True)
    auction_type = models.CharField("Auction type", max_length=5, choices=AUCTION_TYPES, default=ENGLISH_AUCTION)
    start = models.DateTimeField("Start date")
    end = models.DateTimeField("End date")
    active = models.BooleanField("Active", default=False)
    reserve_price = MoneyField("Reserve price", max_digits=10, decimal_places=2, default_currency='CHF')
    reserve_price_posted = models.BooleanField("Is reserve price posted?", default=False)
    minimum_bid = MoneyField("Minimum bid", max_digits=10, decimal_places=2, default_currency='CHF')
    bid_increment = MoneyField("Minimum bid increment", max_digits=10, decimal_places=2, default_currency='CHF')
    dynamic_closing = models.BooleanField("Auction dynamic closing", default=False)
    closing_increment = models.TimeField("Auction dynamic closing time increment", default=time(0, 10, 0))
    total_bids = models.PositiveIntegerField("Total bids", default=0)
    date_added = models.DateTimeField("Date added", auto_now_add=True)
    last_modified = models.DateTimeField("Last modified", auto_now=True)

    class Meta:
        verbose_name = 'Auction'
        verbose_name_plural = 'Auctions'

    @property
    def is_locked(self):
        """
        Bid baskets check this method to find out if a bid can be manipulated.
        """
        now = get_current_time()
        if self.end <= now:
            return True
        return False

    def get_absolute_url(self):
        return reverse('auctions:auction_detail', kwargs={'slug': self.lot.slug})

    @property
    def slug(self):
        return self.lot.slug

    def __unicode__(self):
        return self.lot.title


class BidBasket(models.Model):
    """
    This models functions similarly to a shopping cart, except it expects a logged in user.
    """
    bidder = models.OneToOneField(User, verbose_name="Bidder", blank=False, db_index=True)
    date_added = models.DateTimeField('Date added', auto_now_add=True)
    last_modified = models.DateTimeField('Last modified', auto_now=True)

    class Meta:
        verbose_name = 'Bid basket'
        verbose_name_plural = 'Bid baskets'

    def add_bid(self, auction, amount):
        if auction.is_locked:
            return False

        try:
            amount = Decimal(amount)
        except Exception, e:
            amount = Decimal('0')

        bid = Bid.objects.get_or_create(auction=auction, bid_basket=self)
        if bid:
            bid.amount = amount
            bid.save()
            self.save()
        return bid

    def update_bid(self, auction, amount):
        """
        Update amount of bid. Delete bid if amount is 0.
        """
        try:
            amount = Decimal(amount)
        except Exception, e:
            amount = Decimal('0')

        bid = Bid.objects.get(bid_busket=self, auction=auction)
        if not bid.is_locked():
            if amount == 0:
                bid.delete()
            else:
                bid.amount = amount
                bid.save()
            self.save()
        return bid

    def delete_bid(self, auction):
        """
        Delete a single item from bid basket.
        """
        bid = Bid.objects.get(bid_busket=self, auction=auction)
        if not bid.is_locked():
            bid.delete()
            self.save()
        return bid

    def empty(self):
        """
        Remove all bids from bid basket.
        """
        Bid.objects.filter(bid_busket=self, is_locked=False).delete()
        self.save()

    @property
    def total_bids(self):
        """
        Returns total bids in basket.
        """
        return Bid.objects.filter(bid_busket=self).count()


class Bid(models.Model):
    auction = models.ForeignKey(Auction, verbose_name="Auction", blank=False, db_index=True)
    bid_basket = models.ForeignKey(BidBasket, verbose_name="Bid basket", blank=False)
    amount = MoneyField('Amount', max_digits=10, decimal_places=2, default_currency='CHF')

    class Meta:
        verbose_name = 'Bid'
        verbose_name_plural = 'Bids'

    @property
    def is_locked(self):
        return self.auction.is_locked

    @property
    def lot(self):
        return self.auction.lot