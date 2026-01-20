from rest_framework.routers import DefaultRouter

from .views import DealViewSet, StoreViewSet

router = DefaultRouter()
router.register(r"stores", StoreViewSet, basename="store")
router.register(r"deals", DealViewSet, basename="deal")
urlpatterns = router.urls
