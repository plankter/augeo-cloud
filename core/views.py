from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from braces.views import LoginRequiredMixin

from .models import Artwork
from .forms import PhotoForm, ArtworkForm


class ArtworkList(ListView):
    template_name = 'artwork_list.html'
    context_object_name = 'artworks'
    paginate_by = 50

    def get_queryset(self):
        return Artwork.objects.all()


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
    template_name = 'artwork_detail.html'
    context_object_name = 'artwork'

    def get_context_data(self, **kwargs):
        context = super(ArtworkDetail, self).get_context_data(**kwargs)
        try:
            auction = self.object.auction
        except ObjectDoesNotExist:
            auction = None
        context['auction'] = auction
        return context


class ArtworkUpdate(LoginRequiredMixin, UpdateView):
    model = Artwork
    form_class = ArtworkForm
    template_name = 'artwork_edit.html'
    context_object_name = 'artwork'

    def get_object(self, queryset=None):
        return Artwork.objects.get(slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse_lazy('core:artwork_detail', kwargs={'slug': self.object.slug})


class ArtworkDelete(LoginRequiredMixin, DeleteView):
    model = Artwork
    success_url = reverse_lazy('core:home')