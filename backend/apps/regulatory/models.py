from django.conf import settings
from django.db import models

from apps.common.models import StudyScopedModel, TenantModel


class EthicsCommittee(TenantModel):
    name = models.CharField(max_length=180)
    kind = models.CharField(max_length=24, default="irb")
    country = models.ForeignKey("tenants.Country", null=True, blank=True, on_delete=models.SET_NULL)
    city = models.CharField(max_length=120, blank=True)
    contact_email = models.EmailField(blank=True)
    is_central = models.BooleanField(default=False)


class Submission(StudyScopedModel):
    class Kind(models.TextChoices):
        INITIAL = "initial", "Initial review"
        AMENDMENT = "amendment", "Amendment"
        ANNUAL = "annual", "Annual report"
        SAFETY = "safety", "Safety update"
        CLOSURE = "closure", "Study closure"

    committee = models.ForeignKey(EthicsCommittee, null=True, blank=True, on_delete=models.SET_NULL, related_name="submissions")
    country = models.ForeignKey("tenants.Country", null=True, blank=True, on_delete=models.SET_NULL)
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.INITIAL)
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=24, default="draft")
    submitted_on = models.DateField(null=True, blank=True)
    decision_on = models.DateField(null=True, blank=True)
    reference = models.CharField(max_length=80, blank=True)
    notes = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)


class Approval(StudyScopedModel):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="approvals")
    number = models.CharField(max_length=80)
    approved_on = models.DateField()
    expires_on = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default="active")
    conditions = models.TextField(blank=True)


class RegulatoryObligation(StudyScopedModel):
    country = models.ForeignKey("tenants.Country", null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=180)
    due_date = models.DateField()
    status = models.CharField(max_length=20, default="open")
    authority = models.CharField(max_length=140, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    notes = models.TextField(blank=True)
