from rest_framework import serializers

from .models import Deal, Store,Subscriber,Subscription


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "name", "external_id"]


class DealSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source="store.name", read_only=True)

    class Meta:
        model = Deal
        fields = [
            "id",
            "title",
            "external_id",
            "store",
            "store_name",
            "normal_price",
            "sale_price",
            "currency",
            "discount_percent",
            "url",
            "last_seen_at",
            "is_active",
        ]


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['id','telegram_chat_id']



class SubscriptionSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.name',read_only=True)
    chat_id = serializers.IntegerField(source='telegram_user.telegram_chat_id',read_only=True)

    class Meta:
        model = Subscription
        fields = ['id','telegram_user','chat_id','store','min_discount','max_price','query','is_active']
