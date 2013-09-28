import json

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt

from pure_pagination.mixins import PaginationMixin
from braces.views import LoginRequiredMixin

from .models import Artwork
from .forms import PhotoForm, ArtworkForm, ArtworkPhotoFormSet


class ArtworkCreate(LoginRequiredMixin, CreateView):
    model = Artwork
    template_name = 'artwork_add.html'
    form_class = ArtworkForm

    def form_valid(self, form):
        form.instance.submitter = self.request.user
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return HttpResponseRedirect(self.object.get_absolute_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    #def form_valid(self, form):
    #    form.instance.submitter = self.request.user
    #    return super(ArtworkCreate, self).form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(ArtworkCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ArtworkPhotoFormSet(self.request.POST, instance=self.object)
            context['formset'].full_clean()
        else:
            context['formset'] = ArtworkPhotoFormSet(instance=self.object)
        return context


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