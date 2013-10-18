from decimal import Decimal

from django.http import Http404

from rest_framework import viewsets, serializers, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.permissions import IsAuthenticatedNotOwner
from core.api import ArtworkSerializer
from .models import Auction, BidBasket


class BidSerializer(serializers.Serializer):
    amount = serializers.DecimalField()


class AuctionSerializer(serializers.ModelSerializer):
    lot = ArtworkSerializer(many=False)
    class Meta:
        model = Auction
        fields = ('lot', 'active', 'start', 'end', 'created', 'modified')


class AuctionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuctionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'

    def get_queryset(self):
        return Auction.objects.all()

    def get_object(self):
        obj = Auction.objects.get_auction(self.kwargs['slug'])
        if not obj:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj

    @action(permission_classes=[IsAuthenticatedNotOwner])
    def bid(self, request, **kwargs):
        user = request.user
        basket, created = BidBasket.objects.get_or_create(bidder=user)
        if basket:
            serializer = BidSerializer(data=request.DATA)
            if serializer.is_valid():
                amount = serializer.data['amount']
                if Decimal(amount):
                    auction = self.get_object()
                    bid = basket.add_bid(auction, amount)
                    return Response({'status': 'Bid accepted'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'Bid not accepted'}, status=status.HTTP_400_BAD_REQUEST)