from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=120)
    external_id = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.external_id}:{self.name}"


class Deal(models.Model):
    title = models.CharField(max_length=200)
    external_id = models.IntegerField(unique=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="deals")
    normal_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    discount_percent = models.IntegerField(default=0)
    url = models.URLField(max_length=500)
    last_seen_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(
                fields=["store", "discount_percent", "sale_price"], name="store_idx"
            )
        ]

    def __str__(self):
        return (
            f"{self.title} - {self.store} - {self.sale_price} - {self.discount_percent}"
        )


class Subscriber(models.Model):
    telegram_chat_id = models.IntegerField(unique=True)


class Subscription(models.Model):
    telegram_user = models.ForeignKey(
        Subscriber,
        on_delete=models.SET_NULL,
        related_name="subscriptions",
        null=True,
        blank=True,
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="watched_subscriptions",
        null=True,
        blank=True,
    )
    min_discount = models.IntegerField(default=0)
    max_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    query = models.CharField(max_length=120, blank=True, default="")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.telegram_user} - {self.store} - {self.max_price} - {self.min_discount} - {self.query} - {self.is_active}"


class NotificationLog(models.Model):
    telegram_user = models.ForeignKey(
        Subscriber, on_delete=models.CASCADE, related_name="notifications"
    )
    deal = models.ForeignKey(
        Deal, on_delete=models.CASCADE, related_name="notifications"
    )
    sent_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["telegram_user", "deal"], name="unique_subscriber_deal"
            )
        ]

    def __str__(self):
        return f"{self.telegram_user} - {self.deal} - {self.sent_at}"
