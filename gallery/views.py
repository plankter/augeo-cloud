import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from cloudinary.forms import cl_init_js_callbacks
from endless_pagination.views import AjaxListView

from .models import Photo
from .forms import PhotoForm, PhotoDirectForm


def filter_nones(d):
    return dict((k,v) for k,v in d.iteritems() if v is not None)


class PhotoList(AjaxListView):
    model = Photo
    template_name = 'list.html'
    page_template = 'list_page.html'
    context_object_name = 'photos'

    defaults = dict(format="jpg", height=150, width=150)
    defaults["class"] = "thumbnail inline"

    # The different transformations to present
    samples = [
        dict(crop="fill", radius=10),
        dict(crop="scale"),
        dict(crop="fit", format="png"),
        dict(crop="thumb", gravity="face"),
        dict(format="png", angle=20, height=None, width=None, transformation=[
            dict(crop="fill", gravity="north", width=150, height=150, effect="sepia"),
        ]),
    ]
    samples = [filter_nones(dict(defaults, **sample)) for sample in samples]

    def get_context_data(self, **kwargs):
        context = super(PhotoList, self).get_context_data(**kwargs)
        context['samples'] = self.samples
        return context


def upload(request):
    context = dict(
        # Form demonstrating backend upload
        backend_form = PhotoForm(),
        # Form demonstrating direct upload
        direct_form = PhotoDirectForm(),
    )
    # When using direct upload - the following call in necessary to update the
    # form's callback url
    cl_init_js_callbacks(context['direct_form'], request)

    if request.method == 'POST':
        # Only backend upload should be posting here
        form = PhotoForm(request.POST, request.FILES)
        context['posted'] = form.instance
        if form.is_valid():
            # Uploads image and creates a model instance for it
            form.save()

    return render(request, 'upload.html', context)


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