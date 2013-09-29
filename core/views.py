import json
from time import timezone

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt

from pure_pagination.mixins import PaginationMixin
from braces.views import LoginRequiredMixin

from .models import Artwork, Photo
from .forms import PhotoForm, ArtworkForm


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


class ArtworkUpdate(UpdateView):
    model = Artwork


class ArtworkDelete(DeleteView):
    model = Artwork
    success_url = reverse_lazy('artworks')


class ArtworkList(PaginationMixin, ListView):
    model = Artwork
    template_name = 'artwork_list.html'
    context_object_name = 'artworks'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(ArtworkList, self).get_context_data(**kwargs)
        context['photos'] = Photo.objects.all()
        return context

@csrf_exempt
def add_artwork(request):
    if request.method == "POST":
        artwork_form = ArtworkForm(request.POST, prefix='artwork')
        photo_form = PhotoForm(request.POST, prefix='photo')
        if artwork_form.is_valid() and photo_form.is_valid():
            artwork_form.instance.submitter = request.user
            new_artwork = artwork_form.save()
            new_photo = photo_form.save(commit=False)
            new_photo.artwork = new_artwork
            new_photo.save()

            return HttpResponseRedirect(new_artwork.get_absolute_url())
    else:
        artwork_form = ArtworkForm(prefix='artwork')
        photo_form = PhotoForm(prefix='photo')
    return render_to_response('artwork_add.html', {'artwork_form': artwork_form, 'photo_form': photo_form})


@csrf_exempt
def direct_upload_complete(request):
    form = PhotoForm(request.POST)
    if form.is_valid():
        # Create a model instance for uploaded image using the provided data
        form.save()
        ret = dict(photo_id=form.instance.id)
    else:
        ret = dict(errors=form.errors)

    return HttpResponse(json.dumps(ret), content_type='application/json')