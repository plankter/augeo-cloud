from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from cloudinary import api
from cloudinary.models import CloudinaryField
from rest_framework.authtoken.models import Token
from taggit.managers import TaggableManager
from uuslug import uuslug




@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


for user in User.objects.all():
    Token.objects.get_or_create(user=user)


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
    artist = models.CharField("Artist", max_length=200, blank=True, db_index=True)
    description = models.TextField("Description", blank=True, null=True)
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, db_index=True)
    published = models.DateTimeField("Published", auto_now_add=True)

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
        return self.tags.names()

    def __unicode__(self):
        return "%s by %s" % (self.title, self.artist)


@receiver(pre_delete, sender=Artwork, dispatch_uid='artwork_pre_delete')
def artwork_pre_delete(sender, instance, using, **kwargs):
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
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='photos')

    objects = PhotoManager()

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)
        key = "photo:%s" % self.artwork.slug
        cache.set(key, self)

    def get_absolute_url(self):
        return self.image.url

    def __unicode__(self):
        try:
            result = self.image.public_id
        except AttributeError:
            result = ''
        return result


@receiver(pre_delete, sender=Photo, dispatch_uid='photo_pre_delete')
def photo_pre_delete(sender, instance, using, **kwargs):
    api.delete_resources([instance.image.public_id])

    key = "photo:%s" % instance.artwork.slug
    cache.delete(key)