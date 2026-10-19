from rest_framework import serializers

from apps.common.api import make_serializer, make_viewset
from apps.inventory.models import AccountabilityLog, InvestigationalProduct, Kit, Shipment, TemperatureExcursion

InvestigationalProductSerializer = make_serializer(InvestigationalProduct)
KitSerializer = make_serializer(
    Kit,
    extra={
        "product_name": serializers.CharField(source="product.name", read_only=True),
        "subject_id": serializers.CharField(source="participant.subject_id", read_only=True, allow_null=True, default=""),
    },
)
ShipmentSerializer = make_serializer(Shipment)
AccountabilityLogSerializer = make_serializer(AccountabilityLog)
TemperatureExcursionSerializer = make_serializer(TemperatureExcursion)

ProductViewSet = make_viewset(InvestigationalProduct, InvestigationalProductSerializer, ["name", "code"], ["study"], "products")
KitViewSet = make_viewset(Kit, KitSerializer, ["kit_number", "lot_number"], ["study", "status"], "kits")
ShipmentViewSet = make_viewset(Shipment, ShipmentSerializer, ["reference", "carrier"], ["status"], "shipments")
AccountabilityViewSet = make_viewset(AccountabilityLog, AccountabilityLogSerializer, ["action"], ["action"], "accountability")
ExcursionViewSet = make_viewset(TemperatureExcursion, TemperatureExcursionSerializer, [], ["impact"], "excursions")
