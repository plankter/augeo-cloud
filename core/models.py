from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse

from cloudinary.models import CloudinaryField
from taggit.managers import TaggableManager



class Artwork(models.Model):
    title = models.CharField("Title", max_length=200, blank=True)
    author = models.CharField("Author", max_length=200, blank=True)
    description = models.TextField("Description", blank=True, null=True)
    published = models.DateTimeField("Published", auto_now_add=True)
    submitter = models.ForeignKey(User, editable=False)

    tags = TaggableManager(blank=True)

    def get_absolute_url(self):
        return reverse('core:artworks')

    def __unicode__(self):
        return "<%s by %s>" % (self.title, self.author)


class Photo(models.Model):
    caption = models.CharField("Caption", max_length=200, blank=True)
    image = CloudinaryField('Image', blank=True)
    artwork = models.ForeignKey(Artwork)

    def get_absolute_url(self):
        return reverse('photo-detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return "<%s:%s>" % (self.caption, public_id)