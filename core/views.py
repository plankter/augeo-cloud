import json

from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt

from pure_pagination.mixins import PaginationMixin
from braces.views import LoginRequiredMixin

from .models import Photo, Artwork
from .forms import PhotoForm, ArtworkForm


def filter_nones(d):
    return dict((k, v) for k, v in d.iteritems() if v is not None)


class ArtworkCreate(LoginRequiredMixin, CreateView):
    model = Artwork
    template_name = 'artwork_form.html'
    form_class = ArtworkForm

    def form_valid(self, form):
        form.instance.submitter = self.request.user
        return super(ArtworkCreate, self).form_valid(form)


class ArtworkUpdate(UpdateView):
    model = Artwork


class ArtworkDelete(DeleteView):
    model = Artwork
    success_url = reverse_lazy('artworks')


class ArtworkList(PaginationMixin, ListView):
    model = Artwork
    template_name = 'artworks.html'
    context_object_name = 'artworks'
    paginate_by = 50


class PhotoList(PaginationMixin, ListView):
    model = Photo
    template_name = 'photos.html'
    context_object_name = 'photos'
    paginate_by = 50


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