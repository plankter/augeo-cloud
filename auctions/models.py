from decimal import Decimal
from datetime import time
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

from djmoney.models.fields import MoneyField

from core.models import Artwork
from .utils import get_current_time




class AuctionManager(models.Manager):
    def get_auction(self, slug):
        key = "auction:%s" % slug
        auction = cache.get(key)
        if not auction:
            try:
                auction = Auction.objects.select_related().get(lot__slug=slug)
            except ObjectDoesNotExist:
                return None
            cache.add(key, auction)
        return auction


class Auction(models.Model):
    ENGLISH_AUCTION = 'EA'
    FIRST_PRICE_SEALED_BID_AUCTION = 'FPSBA'

    AUCTION_TYPES = (
        (ENGLISH_AUCTION, 'English auction'),
        (FIRST_PRICE_SEALED_BID_AUCTION, 'First-price sealed-bid auction'),
    )

    lot = models.OneToOneField(Artwork, verbose_name="Lot", blank=False, db_index=True)
    auction_type = models.CharField("Auction type", max_length=5, choices=AUCTION_TYPES, default=ENGLISH_AUCTION)
    start = models.DateTimeField("Auction start")
    end = models.DateTimeField("Auction end")
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

    objects = AuctionManager()

    class Meta:
        verbose_name = 'Auction'
        verbose_name_plural = 'Auctions'

    def save(self, *args, **kwargs):
        super(Auction, self).save(*args, **kwargs)
        key = "auction:%s" % self.lot.slug
        cache.set(key, self)

    def get_absolute_url(self):
        return reverse('auctions:auction_detail', kwargs={'slug': self.lot.slug})

    @property
    def is_locked(self):
        """
        Bid baskets check this method to find out if a bid can be manipulated.
        """
        now = get_current_time()
        if self.end <= now:
            return True
        return False

    def __unicode__(self):
        return self.lot.title


@receiver(post_delete, sender=Auction, dispatch_uid='auction_post_delete')
def auction_post_delete(sender, instance, using, **kwargs):
    key = "auction:%s" % instance.lot.slug
    cache.delete(key)



class BidBasketManager(models.Manager):
    def get_basket(self, user):
        key = "basket:%s" % user.username
        basket = cache.get(key)
        if not basket:
            try:
                basket = BidBasket.objects.get(bidder=user)
            except ObjectDoesNotExist:
                return None
            cache.add(key, basket)
        return basket


class BidBasket(models.Model):
    """
    This models functions similarly to a shopping cart, except it expects a logged in user.
    """
    bidder = models.OneToOneField(User, verbose_name="Bidder", blank=False, db_index=True)
    date_added = models.DateTimeField('Date added', auto_now_add=True)
    last_modified = models.DateTimeField('Last modified', auto_now=True)

    objects = BidBasketManager()

    class Meta:
        verbose_name = 'Bid basket'
        verbose_name_plural = 'Bid baskets'

    def save(self, *args, **kwargs):
        super(BidBasket, self).save(*args, **kwargs)
        key = "basket:%s" % self.bidder.username
        cache.set(key, self)

    def add_bid(self, auction, amount):
        if auction.is_locked:
            return False

        try:
            amount = Decimal(amount)
        except Exception, e:
            amount = Decimal('0')

        bid, created = Bid.objects.get_or_create(bid_basket=self, auction=auction)
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

    def get_notification_channels(self):
        """
        Returns total bids in basket.
        """
        bids = self.bid_set.select_related()
        if bids:
            auctions = [bid.auction for bid in bids]
            slugs = [auction.lot.slug for auction in auctions]
            return ', '.join(slugs)
        return None




class Bid(models.Model):
    auction = models.ForeignKey(Auction, verbose_name="Auction", blank=False, db_index=True)
    bid_basket = models.ForeignKey(BidBasket, verbose_name="Bid basket", blank=False)
    amount = MoneyField('Amount', max_digits=10, decimal_places=2, default_currency='CHF')

    class Meta:
        verbose_name = 'Bid'
        verbose_name_plural = 'Bids'

    def save(self, *args, **kwargs):
        super(Bid, self).save(*args, **kwargs)
        cache.set("bid:" + self.id, self)

    @property
    def is_locked(self):
        return self.auction.is_locked

    @property
    def lot(self):
        return self.auction.lot