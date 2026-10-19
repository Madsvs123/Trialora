from django.contrib import admin

from apps.inventory.models import InvestigationalProduct, Kit, Shipment

admin.site.register(InvestigationalProduct)
admin.site.register(Kit)
admin.site.register(Shipment)
