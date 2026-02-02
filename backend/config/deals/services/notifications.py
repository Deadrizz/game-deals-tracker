import random
from datetime import timedelta
from decimal import Decimal
from django.utils import timezone

from deals.models import Deal, Store,Subscription,NotificationLog




def noti_demo_telegram()->int:
    created_logs = 0
    subscription = Subscription.objects.filter(is_active=True)
    for sub in subscription:
        deals = Deal.objects.filter(is_active=True)
        if sub.store:
            deals = deals.filter(store=sub.store)
        deals = deals.filter(discount_percent__gte=sub.min_discount)
        if sub.max_price:
            deals = deals.filter(sale_price__lte=sub.max_price)
        if sub.query:
            deals = deals.filter(title__icontains=sub.query)
        deals = deals.exclude(notifications__telegram_user=sub.telegram_user)
        for deal in deals:
            notification,was_created = NotificationLog.objects.update_or_create(telegram_user=sub.telegram_user,deal=deal)
            if was_created:
                created_logs+=1
    return created_logs

