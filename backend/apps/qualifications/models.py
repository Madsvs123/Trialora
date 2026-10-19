from django.conf import settings
from django.db import models

from apps.common.models import TenantModel


class StaffCredential(TenantModel):
    class Kind(models.TextChoices):
        LICENSE = "license", "License"
        CERTIFICATION = "certification", "Certification"
        CV = "cv", "Curriculum vitae"
        TRAINING = "training", "Training"
        GCP = "gcp", "GCP"
        MEDICAL = "medical", "Medical credential"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="credentials")
    kind = models.CharField(max_length=24, choices=Kind.choices)
    name = models.CharField(max_length=160)
    issuer = models.CharField(max_length=160, blank=True)
    identifier = models.CharField(max_length=80, blank=True)
    issued_on = models.DateField(null=True, blank=True)
    expires_on = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default="valid")
    document = models.ForeignKey("documents.Document", null=True, blank=True, on_delete=models.SET_NULL)


class TrainingRecord(TenantModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="trainings")
    study = models.ForeignKey("studies.Study", null=True, blank=True, on_delete=models.CASCADE)
    course = models.CharField(max_length=180)
    required = models.BooleanField(default=True)
    due_date = models.DateField(null=True, blank=True)
    completed_on = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default="assigned")
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
