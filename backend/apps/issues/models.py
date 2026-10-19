from django.conf import settings
from django.db import models

from apps.common.models import StudyScopedModel


class Issue(StudyScopedModel):
    class Severity(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    class Kind(models.TextChoices):
        DEVIATION = "deviation", "Protocol deviation"
        ISSUE = "issue", "Operational issue"
        QUERY = "query", "Data query"
        SAFETY = "safety", "Safety signal"

    study_site = models.ForeignKey("sites.StudySite", null=True, blank=True, on_delete=models.SET_NULL)
    participant = models.ForeignKey("participants.Participant", null=True, blank=True, on_delete=models.SET_NULL)
    visit = models.ForeignKey("visits.Visit", null=True, blank=True, on_delete=models.SET_NULL)
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.ISSUE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=80, blank=True)
    severity = models.CharField(max_length=16, choices=Severity.choices, default=Severity.MEDIUM)
    root_cause = models.TextField(blank=True)
    status = models.CharField(max_length=24, default="open")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    due_date = models.DateField(null=True, blank=True)
    resolved_at = models.DateField(null=True, blank=True)
    resolution = models.TextField(blank=True)


class ProtocolDeviation(StudyScopedModel):
    issue = models.OneToOneField(Issue, on_delete=models.CASCADE, related_name="deviation")
    is_important = models.BooleanField(default=False)
    reported_to_irb = models.BooleanField(default=False)
    reported_on = models.DateField(null=True, blank=True)
    protocol_section = models.CharField(max_length=80, blank=True)


class CorrectiveAction(StudyScopedModel):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="actions")
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default="open")
    completed_at = models.DateField(null=True, blank=True)
    preventive = models.BooleanField(default=False)


class Escalation(StudyScopedModel):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="escalations")
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    reason = models.TextField()
    level = models.CharField(max_length=40, default="study_manager")
    created_note = models.CharField(max_length=200, blank=True)
