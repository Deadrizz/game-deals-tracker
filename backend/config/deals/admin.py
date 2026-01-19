from django.contrib import admin
from .models import Store,Deal


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'store',
        'sale_price',
        'discount_percent',
        'is_active',
        'last_seen_at'
    ]
    list_filter = ['store','is_active']
    search_fields = ['title']
    ordering = ['-discount_percent','sale_price']


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name','external_id']
    search_fields = ['name']

