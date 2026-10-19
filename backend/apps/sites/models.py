from django.conf import settings
from django.db import models

from apps.common.models import StudyScopedModel, TenantModel


class Site(TenantModel):
    name = models.CharField(max_length=180)
    site_number = models.CharField(max_length=40, blank=True)
    institution = models.CharField(max_length=200, blank=True)
    country = models.ForeignKey("tenants.Country", null=True, blank=True, on_delete=models.SET_NULL)
    city = models.CharField(max_length=120, blank=True)
    address = models.CharField(max_length=240, blank=True)
    department = models.ForeignKey("tenants.Department", null=True, blank=True, on_delete=models.SET_NULL)
    principal_investigator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="pi_sites",
    )
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    beds = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("organization", "name")
        ordering = ["name"]


class StudySite(StudyScopedModel):
    class Status(models.TextChoices):
        IDENTIFIED = "identified", "Identified"
        FEASIBILITY = "feasibility", "Feasibility"
        SELECTED = "selected", "Selected"
        CONTRACTING = "contracting", "Contracting"
        ACTIVATING = "activating", "Activating"
        ACTIVE = "active", "Active"
        ENROLLING = "enrolling", "Enrolling"
        CLOSED = "closed", "Closed"
        WITHDRAWN = "withdrawn", "Withdrawn"

    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="study_participations")
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.IDENTIFIED)
    activation_date = models.DateField(null=True, blank=True)
    close_date = models.DateField(null=True, blank=True)
    enrollment_target = models.PositiveIntegerField(default=0)
    screening_target = models.PositiveIntegerField(default=0)
    contract_status = models.CharField(max_length=40, blank=True)
    monitoring_status = models.CharField(max_length=40, default="routine")
    investigator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="investigator_study_sites",
    )

    class Meta:
        unique_together = ("study", "site")


class FeasibilityAssessment(StudyScopedModel):
    study_site = models.ForeignKey(StudySite, on_delete=models.CASCADE, related_name="feasibility_assessments")
    status = models.CharField(max_length=24, default="draft")
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    population_fit = models.PositiveIntegerField(default=0)
    staff_readiness = models.PositiveIntegerField(default=0)
    facility_score = models.PositiveIntegerField(default=0)
    competition_risk = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    completed_at = models.DateField(null=True, blank=True)
    assessor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)


class SiteContract(StudyScopedModel):
    study_site = models.ForeignKey(StudySite, on_delete=models.CASCADE, related_name="contracts")
    title = models.CharField(max_length=180)
    status = models.CharField(max_length=24, default="draft")
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=8, default="USD")
    executed_at = models.DateField(null=True, blank=True)
    expires_at = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)


class SiteContact(TenantModel):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField(max_length=140)
    role = models.CharField(max_length=80, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    is_primary = models.BooleanField(default=False)


class SiteQualification(TenantModel):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="qualifications")
    kind = models.CharField(max_length=80)
    status = models.CharField(max_length=24, default="pending")
    completed_at = models.DateField(null=True, blank=True)
    expires_at = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)


class SiteMetric(StudyScopedModel):
    study_site = models.OneToOneField(StudySite, on_delete=models.CASCADE, related_name="metrics")
    screened = models.PositiveIntegerField(default=0)
    enrolled = models.PositiveIntegerField(default=0)
    screen_failed = models.PositiveIntegerField(default=0)
    withdrawn = models.PositiveIntegerField(default=0)
    completed = models.PositiveIntegerField(default=0)
    open_findings = models.PositiveIntegerField(default=0)
    deviations = models.PositiveIntegerField(default=0)
    query_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    enrollment_pace = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    last_refreshed = models.DateTimeField(null=True, blank=True)
