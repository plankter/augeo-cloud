from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from pure_pagination.mixins import PaginationMixin
from braces.views import LoginRequiredMixin

from core.models import Artwork
from .models import Auction, Bid
from .forms import AuctionForm, BidForm


class AuctionList(PaginationMixin, ListView):
    template_name = 'auction_list.html'
    context_object_name = 'auctions'
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
    template_name = 'auction_detail.html'
    context_object_name = 'auction'

    def get_object(self, queryset=None):
        return Auction.objects.select_related().get(lot__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(AuctionDetail, self).get_context_data(**kwargs)
        context['lot'] = Artwork.objects.select_related().get(slug=self.kwargs['slug'])
        return context


class AuctionUpdate(LoginRequiredMixin, UpdateView):
    model = Auction
    form_class = AuctionForm
    template_name = 'auction_edit.html'
    context_object_name = 'auction'

    def get_object(self, queryset=None):
        return Auction.objects.get(lot__slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse_lazy('auctions:auction_detail', kwargs={'slug': self.object.slug})


class AuctionDelete(LoginRequiredMixin, DeleteView):
    model = Auction
    success_url = reverse_lazy('auctions:auction_list')