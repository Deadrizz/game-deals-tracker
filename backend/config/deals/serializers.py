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
        fields = ['id','chat_id','store','store_name','min_discount','max_price','query','is_active']


    def validate_max_price(self,value):
        if value is not None:
            if value<=0:
                raise serializers.ValidationError('Max price should be positive number')
        return value

    def validate_min_discount(self,value):
        if value > 100 or value < 0:
            raise serializers.ValidationError('Min discount should be from 0% to 100%')
        return value