from django.forms import ModelForm

from cloudinary.forms import CloudinaryJsFileField

from .models import Photo, Artwork


class PhotoForm(ModelForm):
    image = CloudinaryJsFileField(
        options={
            'eager': [{'crop': 'fit', 'width': 240}]
        })

    class Meta:
        model = Photo


class ArtworkForm(ModelForm):
    class Meta:
        model = Artwork