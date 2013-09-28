from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from cloudinary.forms import CloudinaryJsFileField

from .models import Photo, Artwork


class ArtworkForm(ModelForm):
    class Meta:
        model = Artwork


class PhotoForm(ModelForm):
    image = CloudinaryJsFileField(
        options={
            'eager': [{'crop': 'fit', 'width': 240}]
        })

    class Meta:
        model = Photo


ArtworkPhotoFormSet = inlineformset_factory(Artwork, Photo, form=PhotoForm)