from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from braces.views import LoginRequiredMixin

from core.models import Artwork
from .models import Auction, BidBasket
from .forms import AuctionForm


class AuctionList(ListView):
    paginate_by = 50

    def get_queryset(self):
        return Auction.objects.select_related()


class AuctionCreate(LoginRequiredMixin, CreateView):
    model = Auction
    template_name = 'auction_add.html'
    form_class = AuctionForm

    def get_context_data(self, **kwargs):
        context = super(AuctionCreate, self).get_context_data(**kwargs)
        context['lot'] = Artwork.objects.get(slug=self.kwargs['slug'])
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form.instance.lot = context['lot']
        self.object = form.save()
        return HttpResponseRedirect(self.object.get_absolute_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class AuctionDetail(DetailView):
    model = Auction

    def get_object(self, queryset=None):
        return Auction.objects.select_related().get(lot__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(AuctionDetail, self).get_context_data(**kwargs)
        lot = Artwork.objects.get(slug=self.kwargs['slug'])
        context['lot'] = lot
        context['photo'] = lot.get_photo()
        if self.request.user.is_authenticated():
            try:
                bid_basket = self.request.user.bidbasket
                if bid_basket:
                    context['notification_channels'] = bid_basket.get_notification_channels()
            except ObjectDoesNotExist:
                pass

        return context


class AuctionUpdate(LoginRequiredMixin, UpdateView):
    model = Auction
    form_class = AuctionForm
    template_name = 'auction_edit.html'

    def get_context_data(self, **kwargs):
        context = super(AuctionUpdate, self).get_context_data(**kwargs)
        context['lot'] = Artwork.objects.get(slug=self.kwargs['slug'])
        return context

    def get_object(self, queryset=None):
        return Auction.objects.get(lot__slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse_lazy('auctions:auction_detail', kwargs={'slug': self.object.slug})


class AuctionDelete(LoginRequiredMixin, DeleteView):
    model = Auction
    success_url = reverse_lazy('auctions:auction_list')

    def get_object(self, queryset=None):
        return Auction.objects.get(lot__slug=self.kwargs['slug'])


class BidView(LoginRequiredMixin, RedirectView):

    def post(self, request, *args, **kwargs):
        user = request.user
        bid_basket, created = BidBasket.objects.get_or_create(bidder=user)
        if bid_basket:
            amount = request.POST['amount']
            if Decimal(amount):
                auction = Auction.objects.get(lot__slug=kwargs['slug'])
                bid = bid_basket.add_bid(auction, amount)
        return super(BidView, self).post(request, *args, **kwargs)

    def get_redirect_url(self, slug):
        return reverse_lazy('auctions:auction_detail', kwargs={'slug': slug})

