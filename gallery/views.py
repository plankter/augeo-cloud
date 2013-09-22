import json

from django.http import HttpResponse
from django.views.generic import ListView
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from cloudinary.forms import cl_init_js_callbacks
from pure_pagination.mixins import PaginationMixin

from .models import Photo
from .forms import PhotoDirectForm


def filter_nones(d):
    return dict((k,v) for k,v in d.iteritems() if v is not None)


class PhotoList(PaginationMixin, ListView):
    model = Photo
    template_name = 'list.html'
    context_object_name = 'photos'
    paginate_by = 50


@csrf_exempt
def direct_upload_complete(request):
    form = PhotoDirectForm(request.POST)
    if form.is_valid():
        # Create a model instance for uploaded image using the provided data
        form.save()
        ret = dict(photo_id = form.instance.id)
    else:
        ret = dict(errors = form.errors)

    return HttpResponse(json.dumps(ret), content_type='application/json')