from rest_framework import viewsets, serializers

from .models import Artwork


class ArtworkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artwork
        fields = ('title', 'artist', 'description',)


class ArtworkViewSet(viewsets.ModelViewSet):
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer