import floppyforms as forms
from cloudinary.forms import CloudinaryJsFileField

from .models import Photo, Artwork


class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ('title','artist','description','tags',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title of the artwork'}),
            'artist': forms.TextInput(attrs={'placeholder': 'Artist name'}),
            'description': forms.Textarea,
        }


class PhotoForm(forms.ModelForm):
    image = CloudinaryJsFileField(
        attrs = { 'style': "display:none", 'id': "id_photo-image" },
        options={
            'tags': ["augeo", "photo"],
            'eager': [{'crop': 'fit', 'width': 240}]
        })

    class Meta:
        model = Photo
        fields = ('image',)


class ContactForm(forms.Form):

    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea)