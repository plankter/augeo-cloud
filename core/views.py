from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from braces.views import LoginRequiredMixin

from auctions.models import Auction
from .models import Artwork
from .forms import PhotoForm, ArtworkForm, ContactForm




class ArtworkList(ListView):
    paginate_by = 50

    def get_queryset(self):
        return Artwork.objects.all()


class ArtworkTaggedList(ListView):
    paginate_by = 50

    def get_queryset(self):
        tag = self.kwargs['tag']
        return Artwork.objects.filter(tags__name__in=[tag])


class ArtworkCreate(LoginRequiredMixin, CreateView):
    model = Artwork
    template_name = 'artwork_add.html'
    form_class = ArtworkForm

    def form_valid(self, form):
        form.instance.submitter = self.request.user
        context = self.get_context_data()
        photo_form = context['photo_form']
        if photo_form.is_valid():
            self.object = form.save()
            new_photo = photo_form.save(commit=False)
            new_photo.artwork = self.object
            new_photo.save()
            return HttpResponseRedirect(self.object.get_absolute_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(ArtworkCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['photo_form'] = PhotoForm(self.request.POST, prefix='photo')
        else:
            context['photo_form'] = PhotoForm(prefix='photo')
        return context


class ArtworkDetail(DetailView):
    model = Artwork

    def get_object(self, queryset=None):
        artwork = Artwork.objects.get_artwork(self.kwargs['slug'])
        return artwork

    def get_context_data(self, **kwargs):
        context = super(ArtworkDetail, self).get_context_data(**kwargs)
        auction = Auction.objects.get_auction(self.object.slug)
        context['auction'] = auction
        return context


class ArtworkUpdate(LoginRequiredMixin, UpdateView):
    model = Artwork
    form_class = ArtworkForm
    template_name = 'artwork_edit.html'

    def get_object(self, queryset=None):
        artwork = Artwork.objects.get_artwork(self.kwargs['slug'])
        return artwork

    def get_success_url(self):
        return reverse_lazy('core:artwork_detail', kwargs={'slug': self.object.slug})


class ArtworkDelete(LoginRequiredMixin, DeleteView):
    model = Artwork
    success_url = reverse_lazy('core:home')




class ContactFormView(FormView):
    form_class = ContactForm
    template_name = "contact_form.html"
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        message = "{name} / {email} said: ".format(
            name=form.cleaned_data.get('name'),
            email=form.cleaned_data.get('email'))
        message += form.cleaned_data.get('message')
        send_mail(
            subject=form.cleaned_data.get('subject').strip(),
            message=message,
            from_email='contact@augeo-cloud.herokuapp.com',
            recipient_list=['Anton Rau <anton.rau@gmail.com>'],
        )
        return super(ContactFormView, self).form_valid(form)