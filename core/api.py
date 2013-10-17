from rest_framework import viewsets, serializers, permissions
from rest_framework.relations import RelatedField

from .models import Artwork




class ArtworkSerializer(serializers.ModelSerializer):
    photos = RelatedField(many=True)
    tags = RelatedField(many=True)
    publisher = RelatedField(many=False)
    class Meta:
        model = Artwork
        fields = ('title', 'slug', 'artist', 'description', 'publisher', 'published', 'tags', 'photos')


class ArtworkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)