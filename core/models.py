from django.db import models

from cloudinary.models import CloudinaryField
from taggit.managers import TaggableManager

from accounts.models import User


class Photo(models.Model):
    caption = models.CharField("Caption (optional)", max_length=200, blank=True)
    image = CloudinaryField('image')

    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return "Photo <%s:%s>" % (self.caption, public_id)


class Artwork(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    submitter = models.ForeignKey(User)
    title = models.CharField("Title (optional)", max_length=200, blank=True)
    author = models.CharField("Author (optional)", max_length=200, blank=True)
    description = models.TextField(blank=True, null=True)
    photos = models.ManyToManyField(Photo, related_name='photos')

    tags = TaggableManager()


    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return "Photo <%s:%s>" % (self.title, public_id)