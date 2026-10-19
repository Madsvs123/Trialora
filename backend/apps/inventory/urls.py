from rest_framework.routers import DefaultRouter

from apps.inventory.views import AccountabilityViewSet, ExcursionViewSet, KitViewSet, ProductViewSet, ShipmentViewSet

router = DefaultRouter()
router.register("products", ProductViewSet, basename="products")
router.register("kits", KitViewSet, basename="kits")
router.register("shipments", ShipmentViewSet, basename="shipments")
router.register("accountability", AccountabilityViewSet, basename="accountability")
router.register("excursions", ExcursionViewSet, basename="excursions")
urlpatterns = router.urls
