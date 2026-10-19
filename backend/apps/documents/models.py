from django.conf import settings
from django.db import models

from apps.common.models import TenantModel


class Document(TenantModel):
    class Category(models.TextChoices):
        PROTOCOL = "protocol", "Protocol"
        IB = "investigator_brochure", "Investigator brochure"
        ICF = "consent", "Informed consent"
        SITE = "site", "Site document"
        CONTRACT = "contract", "Contract"
        APPROVAL = "approval", "Approval"
        CERTIFICATION = "certification", "Certification"
        TRAINING = "training", "Training"
        CORRESPONDENCE = "correspondence", "Correspondence"
        TMF = "tmf", "Trial master file"
        ISF = "isf", "Investigator site file"

    study = models.ForeignKey("studies.Study", null=True, blank=True, on_delete=models.CASCADE, related_name="documents")
    site = models.ForeignKey("sites.Site", null=True, blank=True, on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=32, choices=Category.choices, default=Category.TMF)
    status = models.CharField(max_length=20, default="current")
    expires_at = models.DateField(null=True, blank=True)
    access_roles = models.JSONField(default=list, blank=True)
    current_version = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)


class DocumentVersion(TenantModel):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="versions")
    version = models.PositiveIntegerField()
    file = models.FileField(upload_to="documents/%Y/%m/", blank=True)
    file_name = models.CharField(max_length=200, blank=True)
    change_notes = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ("document", "version")
        ordering = ["-version"]
