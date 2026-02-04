from deals.models import Deal, NotificationLog, Subscriber, Subscription


def noti_demo_telegram(chat_id: int | None) -> int:
    created_logs = 0
    if chat_id is not None:
        subscription = Subscription.objects.filter(
            telegram_user__telegram_chat_id=chat_id, is_active=True
        )
    else:
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
            notification, was_created = NotificationLog.objects.update_or_create(
                telegram_user=sub.telegram_user, deal=deal
            )
            if was_created:
                created_logs += 1
    return created_logs


def send_notification(chat_id: int):
    result = []
    sent_ids = []
    subscriber = Subscriber.objects.get(telegram_chat_id=chat_id)
    notifications = NotificationLog.objects.filter(
        telegram_user=subscriber, is_sent=False
    ).select_related("deal", "deal__store")
    for noti in notifications[:10]:
        sent_ids.append(noti.id)
        noti_dict = {
            "title": noti.deal.title,
            "store": noti.deal.store.name or None,
            "sale_price": noti.deal.sale_price,
            "discount_percent": noti.deal.discount_percent,
            "url": noti.deal.url,
        }
        result.append(noti_dict)
    NotificationLog.objects.filter(id__in=sent_ids).update(is_sent=True)
    return result
