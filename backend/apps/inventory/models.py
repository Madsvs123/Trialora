from django.conf import settings
from django.db import models

from apps.common.models import StudyScopedModel


class InvestigationalProduct(StudyScopedModel):
    name = models.CharField(max_length=160)
    code = models.CharField(max_length=40)
    dosage_form = models.CharField(max_length=80, blank=True)
    strength = models.CharField(max_length=80, blank=True)
    storage_condition = models.CharField(max_length=120, blank=True)
    is_comparator = models.BooleanField(default=False)

    class Meta:
        unique_together = ("study", "code")


class Kit(StudyScopedModel):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        ALLOCATED = "allocated", "Allocated"
        DISPENSED = "dispensed", "Dispensed"
        RETURNED = "returned", "Returned"
        QUARANTINE = "quarantine", "Quarantine"
        DESTROYED = "destroyed", "Destroyed"

    product = models.ForeignKey(InvestigationalProduct, on_delete=models.CASCADE, related_name="kits")
    study_site = models.ForeignKey("sites.StudySite", null=True, blank=True, on_delete=models.SET_NULL, related_name="kits")
    participant = models.ForeignKey("participants.Participant", null=True, blank=True, on_delete=models.SET_NULL, related_name="kits")
    kit_number = models.CharField(max_length=40)
    lot_number = models.CharField(max_length=40, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)

    class Meta:
        unique_together = ("study", "kit_number")


class Shipment(StudyScopedModel):
    study_site = models.ForeignKey("sites.StudySite", on_delete=models.CASCADE, related_name="shipments")
    reference = models.CharField(max_length=80)
    shipped_on = models.DateField(null=True, blank=True)
    received_on = models.DateField(null=True, blank=True)
    carrier = models.CharField(max_length=80, blank=True)
    status = models.CharField(max_length=20, default="planned")
    temperature_ok = models.BooleanField(default=True)
    notes = models.TextField(blank=True)


class AccountabilityLog(StudyScopedModel):
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE, related_name="logs")
    action = models.CharField(max_length=40)
    quantity = models.PositiveIntegerField(default=1)
    performed_on = models.DateTimeField()
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    notes = models.TextField(blank=True)


class TemperatureExcursion(StudyScopedModel):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="excursions")
    recorded_at = models.DateTimeField()
    min_c = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    max_c = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=0)
    impact = models.CharField(max_length=20, default="under_review")
    notes = models.TextField(blank=True)
