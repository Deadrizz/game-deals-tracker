from rest_framework import viewsets

from .filters import DealFilter
from .models import Deal, Store
from .serializers import DealSerializer, StoreSerializer


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class DealViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    filterset_class = DealFilter
    search_fields = ["title"]
    ordering_fields = ["discount_percent", "sale_price", "last_seen_at"]
    ordering = ["-discount_percent", "sale_price"]
