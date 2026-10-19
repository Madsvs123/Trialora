from django.conf import settings
from django.db import models

from apps.common.models import StudyScopedModel


class AdverseEvent(StudyScopedModel):
    class Seriousness(models.TextChoices):
        NON_SERIOUS = "non_serious", "Non-serious"
        SERIOUS = "serious", "Serious"

    class Severity(models.TextChoices):
        MILD = "mild", "Mild"
        MODERATE = "moderate", "Moderate"
        SEVERE = "severe", "Severe"
        LIFE_THREATENING = "life_threatening", "Life-threatening"

    class Causality(models.TextChoices):
        UNRELATED = "unrelated", "Unrelated"
        UNLIKELY = "unlikely", "Unlikely"
        POSSIBLE = "possible", "Possible"
        PROBABLE = "probable", "Probable"
        DEFINITE = "definite", "Definite"

    participant = models.ForeignKey("participants.Participant", on_delete=models.CASCADE, related_name="adverse_events")
    study_site = models.ForeignKey("sites.StudySite", null=True, blank=True, on_delete=models.SET_NULL)
    visit = models.ForeignKey("visits.Visit", null=True, blank=True, on_delete=models.SET_NULL)
    ae_number = models.CharField(max_length=40)
    term = models.CharField(max_length=200)
    meddra_code = models.CharField(max_length=40, blank=True)
    onset_date = models.DateField()
    resolved_date = models.DateField(null=True, blank=True)
    seriousness = models.CharField(max_length=20, choices=Seriousness.choices, default=Seriousness.NON_SERIOUS)
    severity = models.CharField(max_length=24, choices=Severity.choices, default=Severity.MILD)
    causality = models.CharField(max_length=20, choices=Causality.choices, default=Causality.POSSIBLE)
    expected = models.BooleanField(default=False)
    outcome = models.CharField(max_length=80, default="ongoing")
    status = models.CharField(max_length=24, default="open")
    narrative = models.TextField(blank=True)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ("study", "ae_number")
        ordering = ["-onset_date"]


class SeriousAdverseEvent(StudyScopedModel):
    adverse_event = models.OneToOneField(AdverseEvent, on_delete=models.CASCADE, related_name="sae")
    criteria = models.JSONField(default=list, blank=True)
    reported_to_sponsor_on = models.DateField(null=True, blank=True)
    reported_to_irb_on = models.DateField(null=True, blank=True)
    reported_to_regulator_on = models.DateField(null=True, blank=True)
    clock_start = models.DateTimeField(null=True, blank=True)
    days_to_report = models.PositiveIntegerField(default=15)
    is_susar = models.BooleanField(default=False)
    follow_up_required = models.BooleanField(default=True)


class SafetyReport(StudyScopedModel):
    adverse_event = models.ForeignKey(AdverseEvent, on_delete=models.CASCADE, related_name="reports")
    report_type = models.CharField(max_length=24, default="cioms")
    destination = models.CharField(max_length=120)
    submitted_on = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default="draft")
    reference = models.CharField(max_length=80, blank=True)
    notes = models.TextField(blank=True)


class SafetySignal(StudyScopedModel):
    name = models.CharField(max_length=180)
    term = models.CharField(max_length=160, blank=True)
    status = models.CharField(max_length=20, default="open")
    events_count = models.PositiveIntegerField(default=0)
    detected_on = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    assessment = models.TextField(blank=True)
