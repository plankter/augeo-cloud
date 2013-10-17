from rest_framework import viewsets, serializers, permissions, status
from rest_framework.decorators import action
from rest_framework.relations import RelatedField
from rest_framework.response import Response

from core.permissions import IsOwnerOrReadOnly
from core.api import ArtworkSerializer
from .models import Auction, Bid




class BidSerializer(serializers.ModelSerializer):
    auction = RelatedField(many=False)
    bid_basket = RelatedField(many=False)
    class Meta:
        model = Bid
        fields = ('auction', 'bid_basket', 'amount')


class AuctionSerializer(serializers.ModelSerializer):
    lot = ArtworkSerializer(many=False)
    class Meta:
        model = Auction
        fields = ('lot', 'active', 'start', 'end', 'created', 'modified')


class AuctionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    @action(permission_classes=[permissions.IsAuthenticated])
    def bid(self, request, pk=None):
        auction = self.get_object()
        serializer = BidSerializer(data=request.DATA)
        if serializer.is_valid():
            #user.set_password(serializer.data['password'])
            #user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)