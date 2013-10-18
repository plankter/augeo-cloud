from django.http import Http404

from rest_framework import viewsets, serializers, permissions
from rest_framework.relations import RelatedField

from .permissions import IsOwnerOrReadOnly
from .models import Artwork


class ArtworkSerializer(serializers.ModelSerializer):
    photos = RelatedField(many=True)
    tags = RelatedField(many=True)
    publisher = RelatedField(many=False)

    class Meta:
        model = Artwork
        fields = ('title', 'slug', 'artist', 'description', 'publisher', 'published', 'tags', 'photos')


class ArtworkViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ArtworkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    lookup_field = 'slug'

    def get_queryset(self):
        return Artwork.objects.all()

    def get_object(self):
        obj = Artwork.objects.get_artwork(self.kwargs['slug'])
        if not obj:
            raise Http404

        self.check_object_permissions(self.request, obj)
        return obj