from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.core.urlresolvers import reverse

from cloudinary import api
from cloudinary.models import CloudinaryField
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from taggit.managers import TaggableManager
from uuslug import uuslug




class ArtworkManager(models.Manager):
    def get_artwork(self, slug):
        key = "artwork:%s" % slug
        artwork = cache.get(key)
        if not artwork:
            artwork = Artwork.objects.select_related().get(slug=slug)
            if artwork:
                cache.add(key, artwork)
        return artwork


class Artwork(models.Model):
    title = models.CharField("Title", max_length=200, blank=False, db_index=True)
    slug = models.SlugField("Slug", max_length=50, blank=False, unique=True, db_index=True)
    artist = models.CharField("Artist", max_length=200, blank=True)
    description = models.TextField("Description", blank=True, null=True)
    published = models.DateTimeField("Published", auto_now_add=True)
    submitter = models.ForeignKey(User, editable=False)

    tags = TaggableManager("Tags", blank=True)

    objects = ArtworkManager()

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self, max_length=50, word_boundary=True)
        super(Artwork, self).save(*args, **kwargs)
        key = "artwork:%s" % self.slug
        cache.set(key, self)

    def get_absolute_url(self):
        return reverse('core:artwork_detail', kwargs={'slug': self.slug})

    def get_photo(self):
        return Photo.objects.get_photo(self)

    def dehydrate_tags(self):
        return map(str, self.tags.all())

    def __unicode__(self):
        return "%s by %s" % (self.title, self.artist)


@receiver(pre_delete, sender=Artwork, dispatch_uid='artwork_pre_delete')
def artwork_pre_delete(sender, instance, using, **kwargs):
    photo = instance.get_photo()
    api.delete_resources([photo.image.public_id])


@receiver(post_delete, sender=Artwork, dispatch_uid='artwork_post_delete')
def artwork_post_delete(sender, instance, using, **kwargs):
    key = "artwork:%s" % instance.slug
    cache.delete(key)




class PhotoManager(models.Manager):
    def get_photo(self, artwork):
        key = "photo:%s" % artwork.slug
        photo = cache.get(key)
        if not photo:
            photo = Photo.objects.get(artwork=artwork)
            if photo:
                cache.add(key, photo)
        return photo


class Photo(models.Model):
    caption = models.CharField("Caption", max_length=200, blank=True)
    image = CloudinaryField("Image", blank=True)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)

    objects = PhotoManager()

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)
        key = "photo:%s" % self.artwork.slug
        cache.set(key, self)

    def get_absolute_url(self):
        return self.image.url

    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return "%s:%s" % (self.caption, public_id)


@receiver(post_delete, sender=Photo, dispatch_uid='photo_post_delete')
def photo_post_delete(sender, instance, using, **kwargs):
    key = "photo:%s" % instance.artwork.slug
    cache.delete(key)