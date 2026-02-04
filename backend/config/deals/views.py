from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from .filters import DealFilter
from .models import Deal, Store,Subscription,Subscriber,NotificationLog
from .serializers import DealSerializer, StoreSerializer,SubscriptionSerializer,SubscriberSerializer
from rest_framework.response import Response
from rest_framework import status
from deals.services.notifications import noti_demo_telegram


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



class SubscriberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer



class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    ordering = ['id','is_active']

    def get_queryset(self):
        chat_id = self.request.GET.get('chat_id')
        if chat_id is None or not chat_id.isdigit():
            return Subscription.objects.none()
        return Subscription.objects.filter(telegram_user__telegram_chat_id=chat_id)

    def perform_create(self,serializer):
        chat_id = self.request.GET.get('chat_id')
        if chat_id is None or not chat_id.isdigit():
            raise ValidationError()
        subscription,_ = Subscriber.objects.get_or_create(telegram_chat_id=chat_id)
        return serializer.save(telegram_user=subscription)


class NotificationLogAPIView(APIView):
    def post(self,request,*args,**kwargs):
        chat_id = request.query_params.get('chat_id')
        if chat_id is None or not chat_id.isdigit():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        created = noti_demo_telegram(int(chat_id))
        return Response({'created':created})
