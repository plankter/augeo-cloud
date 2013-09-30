from django.forms import ModelForm

from cloudinary.forms import CloudinaryJsFileField

from .models import Photo, Artwork


class ArtworkForm(ModelForm):
    class Meta:
        model = Artwork
        exclude = ('slug',)


class PhotoForm(ModelForm):
    image = CloudinaryJsFileField(
        options={
            'tags': ["augeo", "photo"],
            'eager': [{'crop': 'fit', 'width': 240}]
        })

    class Meta:
        model = Photo
        exclude = ('artwork',)