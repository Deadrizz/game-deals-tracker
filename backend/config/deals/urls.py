from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    DealViewSet,
    DispatchNotificationsAPIView,
    NotificationLogAPIView,
    StoreViewSet,
    SubscriberViewSet,
    SubscriptionViewSet,
)

router = DefaultRouter()
router.register(r"stores", StoreViewSet, basename="store")
router.register(r"deals", DealViewSet, basename="deal")
router.register(r"subscriptions", SubscriptionViewSet, basename="subscriptions")
router.register(r"subscribers", SubscriberViewSet, basename="subscribers")
urlpatterns = router.urls + [
    path(
        "notification/generate/", NotificationLogAPIView.as_view(), name="notifications"
    ),
    path(
        "notification/dispatch/",
        DispatchNotificationsAPIView.as_view(),
        name="dispatch",
    ),
]
