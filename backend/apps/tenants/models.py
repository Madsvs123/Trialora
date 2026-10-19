from django.db import models
from django.utils.text import slugify

from apps.common.models import TenantModel, UUIDModel


class Organization(UUIDModel):
    class OrgType(models.TextChoices):
        SPONSOR = "sponsor", "Sponsor"
        CRO = "cro", "CRO"
        HOSPITAL = "hospital", "Hospital"
        RESEARCH = "research", "Research organization"
        ACADEMIC = "academic", "Academic center"

    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=180, unique=True)
    org_type = models.CharField(max_length=24, choices=OrgType.choices, default=OrgType.RESEARCH)
    legal_name = models.CharField(max_length=220, blank=True)
    country = models.CharField(max_length=80, blank=True)
    timezone = models.CharField(max_length=64, default="UTC")
    logo_color = models.CharField(max_length=12, default="#1B4D3E")
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    settings = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:180]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Department(TenantModel):
    name = models.CharField(max_length=140)
    code = models.CharField(max_length=32, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("organization", "name")
        ordering = ["name"]


class Sponsor(TenantModel):
    name = models.CharField(max_length=180)
    code = models.CharField(max_length=40, blank=True)
    contact_name = models.CharField(max_length=140, blank=True)
    contact_email = models.EmailField(blank=True)
    country = models.CharField(max_length=80, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("organization", "name")
        ordering = ["name"]


class Country(UUIDModel):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=120)
    region = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "countries"


class OrganizationSetting(TenantModel):
    enrollment_alert_threshold = models.PositiveIntegerField(default=80)
    document_expiry_days = models.PositiveIntegerField(default=30)
    visit_overdue_grace_days = models.PositiveIntegerField(default=2)
    finding_escalation_days = models.PositiveIntegerField(default=14)
    allow_pii_export = models.BooleanField(default=False)
    default_study_phase = models.CharField(max_length=20, default="II")
    notification_email = models.EmailField(blank=True)
    branding = models.JSONField(default=dict, blank=True)
    status_workflows = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ("organization",)
