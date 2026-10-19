from django.db import models

from apps.common.models import StudyScopedModel


class StudyBudget(StudyScopedModel):
    category = models.CharField(max_length=80)
    planned = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    committed = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    actual = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    currency = models.CharField(max_length=8, default="USD")
    notes = models.TextField(blank=True)


class Payment(StudyScopedModel):
    class Kind(models.TextChoices):
        SITE = "site", "Site payment"
        INVESTIGATOR = "investigator", "Investigator payment"
        MILESTONE = "milestone", "Milestone"
        VENDOR = "vendor", "Vendor"

    study_site = models.ForeignKey("sites.StudySite", null=True, blank=True, on_delete=models.SET_NULL)
    investigator = models.ForeignKey("accounts.User", null=True, blank=True, on_delete=models.SET_NULL)
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.SITE)
    title = models.CharField(max_length=180)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=8, default="USD")
    status = models.CharField(max_length=20, default="scheduled")
    due_date = models.DateField(null=True, blank=True)
    paid_on = models.DateField(null=True, blank=True)
    milestone = models.CharField(max_length=120, blank=True)


class Invoice(StudyScopedModel):
    number = models.CharField(max_length=40)
    payment = models.ForeignKey(Payment, null=True, blank=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=8, default="USD")
    status = models.CharField(max_length=20, default="draft")
    issued_on = models.DateField(null=True, blank=True)
    due_on = models.DateField(null=True, blank=True)


class Expense(StudyScopedModel):
    category = models.CharField(max_length=80)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=8, default="USD")
    incurred_on = models.DateField()
    status = models.CharField(max_length=20, default="submitted")
    vendor = models.CharField(max_length=140, blank=True)
    notes = models.TextField(blank=True)


class Grant(StudyScopedModel):
    source = models.CharField(max_length=160)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    currency = models.CharField(max_length=8, default="USD")
    status = models.CharField(max_length=20, default="active")
    awarded_on = models.DateField(null=True, blank=True)
    ends_on = models.DateField(null=True, blank=True)
    reference = models.CharField(max_length=80, blank=True)
