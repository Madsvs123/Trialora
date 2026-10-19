from django.conf import settings
from django.db import models

from apps.common.models import StudyScopedModel


class MonitoringVisit(StudyScopedModel):
    class Kind(models.TextChoices):
        SIV = "siv", "Site initiation"
        IMV = "imv", "Interim monitoring"
        COV = "cov", "Close-out"
        REMOTE = "remote", "Remote"
        FOR_CAUSE = "for_cause", "For-cause"

    study_site = models.ForeignKey("sites.StudySite", on_delete=models.CASCADE, related_name="monitoring_visits")
    monitor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.IMV)
    scheduled_date = models.DateField()
    actual_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default="planned")
    agenda = models.TextField(blank=True)
    attendees = models.JSONField(default=list, blank=True)


class TripReport(StudyScopedModel):
    monitoring_visit = models.OneToOneField(MonitoringVisit, on_delete=models.CASCADE, related_name="trip_report")
    summary = models.TextField()
    submitted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default="draft")
    recommended_actions = models.TextField(blank=True)


class Finding(StudyScopedModel):
    class Severity(models.TextChoices):
        MINOR = "minor", "Minor"
        MAJOR = "major", "Major"
        CRITICAL = "critical", "Critical"

    monitoring_visit = models.ForeignKey(MonitoringVisit, on_delete=models.CASCADE, related_name="findings")
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    severity = models.CharField(max_length=16, choices=Severity.choices, default=Severity.MINOR)
    category = models.CharField(max_length=80, blank=True)
    status = models.CharField(max_length=20, default="open")
    due_date = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)


class ActionItem(StudyScopedModel):
    finding = models.ForeignKey(Finding, null=True, blank=True, on_delete=models.CASCADE, related_name="actions")
    monitoring_visit = models.ForeignKey(MonitoringVisit, null=True, blank=True, on_delete=models.CASCADE, related_name="actions")
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default="open")
    completed_at = models.DateField(null=True, blank=True)


class FollowUpLetter(StudyScopedModel):
    monitoring_visit = models.ForeignKey(MonitoringVisit, on_delete=models.CASCADE, related_name="letters")
    subject = models.CharField(max_length=180)
    body = models.TextField()
    sent_at = models.DateTimeField(null=True, blank=True)
    recipient = models.CharField(max_length=180, blank=True)


class RiskIndicator(StudyScopedModel):
    study_site = models.ForeignKey("sites.StudySite", on_delete=models.CASCADE, related_name="risk_indicators")
    name = models.CharField(max_length=120)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    trend = models.CharField(max_length=16, default="stable")
    threshold = models.DecimalField(max_digits=5, decimal_places=2, default=5)
    notes = models.TextField(blank=True)
