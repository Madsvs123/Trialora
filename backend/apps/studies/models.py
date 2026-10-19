from django.conf import settings
from django.db import models

from apps.common.models import StudyScopedModel, TenantModel


class Study(TenantModel):
    class Phase(models.TextChoices):
        I = "I", "Phase I"
        I_II = "I/II", "Phase I/II"
        II = "II", "Phase II"
        II_III = "II/III", "Phase II/III"
        III = "III", "Phase III"
        IV = "IV", "Phase IV"
        OBS = "OBS", "Observational"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        STARTUP = "startup", "Start-up"
        ENROLLING = "enrolling", "Enrolling"
        ACTIVE = "active", "Active"
        FOLLOW_UP = "follow_up", "Follow-up"
        CLOSED = "closed", "Closed"
        ON_HOLD = "on_hold", "On hold"

    code = models.CharField(max_length=40)
    title = models.CharField(max_length=240)
    protocol_number = models.CharField(max_length=80, blank=True)
    acronym = models.CharField(max_length=40, blank=True)
    phase = models.CharField(max_length=12, choices=Phase.choices, default=Phase.II)
    therapeutic_area = models.CharField(max_length=140, blank=True)
    indication = models.CharField(max_length=180, blank=True)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.DRAFT)
    sponsor = models.ForeignKey("tenants.Sponsor", null=True, blank=True, on_delete=models.SET_NULL, related_name="studies")
    department = models.ForeignKey("tenants.Department", null=True, blank=True, on_delete=models.SET_NULL, related_name="studies")
    description = models.TextField(blank=True)
    enrollment_target = models.PositiveIntegerField(default=0)
    screening_target = models.PositiveIntegerField(default=0)
    start_date = models.DateField(null=True, blank=True)
    first_patient_in = models.DateField(null=True, blank=True)
    last_patient_in = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    nct_id = models.CharField(max_length=20, blank=True)
    eudra_ct = models.CharField(max_length=40, blank=True)
    custom_fields = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ("organization", "code")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.code} — {self.title}"


class Protocol(StudyScopedModel):
    version = models.CharField(max_length=20)
    title = models.CharField(max_length=240)
    summary = models.TextField(blank=True)
    effective_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=True)
    amendment_number = models.CharField(max_length=20, blank=True)
    approved_at = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-effective_date", "-created_at"]


class StudyMilestone(StudyScopedModel):
    class Status(models.TextChoices):
        PLANNED = "planned", "Planned"
        IN_PROGRESS = "in_progress", "In progress"
        COMPLETE = "complete", "Complete"
        DELAYED = "delayed", "Delayed"

    name = models.CharField(max_length=160)
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    notes = models.TextField(blank=True)
    sequence = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sequence", "due_date"]


class StudyObjective(StudyScopedModel):
    class Kind(models.TextChoices):
        PRIMARY = "primary", "Primary"
        SECONDARY = "secondary", "Secondary"
        EXPLORATORY = "exploratory", "Exploratory"

    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.PRIMARY)
    text = models.TextField()
    endpoint = models.CharField(max_length=240, blank=True)
    sequence = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["kind", "sequence"]


class StudyCountry(StudyScopedModel):
    country = models.ForeignKey("tenants.Country", on_delete=models.PROTECT, related_name="study_countries")
    enrollment_target = models.PositiveIntegerField(default=0)
    regulatory_status = models.CharField(max_length=80, blank=True)
    approved_at = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("study", "country")


class StudyTeamMember(StudyScopedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="study_roles")
    role_label = models.CharField(max_length=80)
    is_lead = models.BooleanField(default=False)

    class Meta:
        unique_together = ("study", "user", "role_label")


class StudyTemplate(TenantModel):
    name = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    phase = models.CharField(max_length=12, default="II")
    therapeutic_area = models.CharField(max_length=140, blank=True)
    default_milestones = models.JSONField(default=list, blank=True)
    default_visits = models.JSONField(default=list, blank=True)
    default_objectives = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)


class CustomField(TenantModel):
    entity_type = models.CharField(max_length=40)
    name = models.CharField(max_length=80)
    field_key = models.SlugField(max_length=80)
    field_type = models.CharField(max_length=20, default="text")
    options = models.JSONField(default=list, blank=True)
    required = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("organization", "entity_type", "field_key")


class StatusWorkflow(TenantModel):
    entity_type = models.CharField(max_length=40)
    name = models.CharField(max_length=80)
    states = models.JSONField(default=list)
    transitions = models.JSONField(default=list)
    is_default = models.BooleanField(default=False)

    class Meta:
        unique_together = ("organization", "entity_type", "name")
