import django_filters

from .models import Deal, Store


class DealFilter(django_filters.FilterSet):
    store = django_filters.ModelChoiceFilter(queryset=Store.objects.all())
    min_discount = django_filters.NumberFilter(
        field_name="discount_percent", lookup_expr="gte"
    )
    max_price = django_filters.NumberFilter(field_name="sale_price", lookup_expr="lte")

    class Meta:
        model = Deal
        fields = ["store", "min_discount", "max_price"]
