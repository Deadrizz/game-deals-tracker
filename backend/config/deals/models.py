from django.db import models

class Store(models.Model):
    name = models.CharField(max_length=120)
    external_id = models.IntegerField(unique=True)
    def __str__(self):
        return f"{self.external_id}:{self.name}"

class Deal(models.Model):
    title = models.CharField(max_length=200)
    external_id = models.IntegerField(unique=True)
    store = models.ForeignKey(Store,on_delete=models.CASCADE,related_name='deals')
    normal_price = models.DecimalField(max_digits=10,decimal_places=2)
    sale_price = models.DecimalField(max_digits=10,decimal_places=2)
    currency = models.CharField(max_length=10)
    discount_percent = models.IntegerField(default=0)
    url = models.URLField(max_length=500)
    last_seen_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        indexes = [models.Index(fields=['store','discount_percent','sale_price'],name='store_idx')]
    def __str__(self):
        return f"{self.title} - {self.store} - {self.sale_price} - {self.discount_percent}"
