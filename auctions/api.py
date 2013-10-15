from rest_framework import viewsets, serializers

from .models import Auction


class AuctionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Auction
        fields = ('lot', 'start', 'end',)


class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer