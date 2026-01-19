from rest_framework import serializers
from .models import Store,Deal


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id','name','external_id']


class DealSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.name',read_only=True)
    class Meta:
        model = Deal
        fields = ['id','title','external_id','store','store_name','normal_price','sale_price','currency','discount_percent','url','last_seen_at','is_active']
