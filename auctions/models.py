from decimal import Decimal
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from south.modelsinspector import add_introspection_rules

from core.models import Artwork
from events.views import pubnub
from .utils import get_current_time




class CurrencyField(models.DecimalField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, verbose_name=None, name=None, **kwargs):
        decimal_places = kwargs.pop('decimal_places', 2)
        max_digits = kwargs.pop('max_digits', 10)

        super(CurrencyField, self). __init__(
            verbose_name=verbose_name, name=name, max_digits=max_digits,
            decimal_places=decimal_places, **kwargs)

    def to_python(self, value):
        try:
            return super(CurrencyField, self).to_python(value).quantize(Decimal("0.01"))
        except AttributeError:
            return None


add_introspection_rules([
    (
            [CurrencyField],
            [],
            {
                "decimal_places": ["decimal_places", {"default": "2"}],
                "max_digits": ["max_digits", {"default": "10"}],
            },
    ), ], ['^application\.fields\.CurrencyField'])




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

    lot = models.OneToOneField(Artwork, verbose_name="Lot", blank=False)
    #auction_type = models.CharField("Auction type", max_length=5, choices=AUCTION_TYPES, default=ENGLISH_AUCTION)
    start = models.DateTimeField("Auction start", blank=False, db_index=True)
    end = models.DateTimeField("Auction end", blank=False, db_index=True)
    active = models.BooleanField("Active", blank=False, default=False)
    #reserve_price = CurrencyField("Reserve price", blank=True)
    #reserve_price_posted = models.BooleanField("Is reserve price posted?", default=False)
    #minimum_bid = CurrencyField("Minimum bid", blank=True)
    #bid_increment = CurrencyField("Minimum bid increment", blank=True)
    #dynamic_closing = models.BooleanField("Auction dynamic closing", default=False)
    #closing_increment = models.TimeField("Auction dynamic closing time increment", default=time(0, 10, 0))
    #total_bids = models.PositiveIntegerField("Total bids", default=0)
    created = models.DateTimeField("Created", auto_now_add=True)
    modified = models.DateTimeField("Modified", auto_now=True)

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


@receiver(pre_delete, sender=Auction, dispatch_uid='auction_pre_delete')
def auction_pre_delete(sender, instance, using, **kwargs):
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
    bidder = models.OneToOneField(User, verbose_name="Bidder", blank=False)
    created = models.DateTimeField('Created', auto_now_add=True)
    modified = models.DateTimeField('Modified', auto_now=True)

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
        except Exception:
            return False

        highest_bid = Bid.objects.get_highest_bid(auction)
        if amount <= highest_bid:
            return False

        bid, created = Bid.objects.get_or_create(bid_basket=self, auction=auction, amount=amount)
        if bid:
            bid.save()
            self.save()

            amount_text = str(amount.quantize(Decimal("0.01")))

            pubnub.publish({
                'channel': auction.lot.slug,
                'message': {
                    'text': 'New bid!',
                    'amount': amount_text
                }
            })

            pubnub.publish({
                'channel': auction.lot.publisher.username,
                'message': {
                    'text': 'New bid %s on <strong>"%s"</strong>' % (amount_text, auction),
                }
            })
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

    def total_bids(self):
        """
        Returns total bids in basket.
        """
        return Bid.objects.filter(bid_busket=self).count()




class BidManager(models.Manager):
    def get_highest_bid(self, auction):
        key = "highest_bid:%s" % auction.lot.slug
        highest_bid = cache.get(key)
        if not highest_bid:
            try:
                highest_bid = Bid.objects.filter(auction=auction).aggregate(models.Max('amount'))['amount__max']
            except ObjectDoesNotExist:
                return None
            cache.add(key, highest_bid)
        return highest_bid


class Bid(models.Model):
    auction = models.ForeignKey(Auction, verbose_name="Auction", blank=False, related_name='bids')
    bid_basket = models.ForeignKey(BidBasket, verbose_name="Bid basket", blank=False, related_name='bids')
    amount = CurrencyField('Amount', blank=False, db_index=True)

    objects = BidManager()

    class Meta:
        verbose_name = 'Bid'
        verbose_name_plural = 'Bids'

    def save(self, *args, **kwargs):
        super(Bid, self).save(*args, **kwargs)
        key = "highest_bid:%s" % self.auction.lot.slug
        cache.set(key, self.amount)