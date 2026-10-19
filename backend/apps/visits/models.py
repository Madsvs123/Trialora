from django.db import models

from apps.common.models import StudyScopedModel


class VisitDefinition(StudyScopedModel):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=24)
    sequence = models.PositiveIntegerField(default=0)
    window_start_days = models.IntegerField(default=0)
    window_end_days = models.IntegerField(default=0)
    is_unscheduled = models.BooleanField(default=False)
    required_forms = models.JSONField(default=list, blank=True)

    class Meta:
        unique_together = ("study", "code")
        ordering = ["sequence"]


class Visit(StudyScopedModel):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        WINDOW = "in_window", "In window"
        COMPLETED = "completed", "Completed"
        MISSED = "missed", "Missed"
        OVERDUE = "overdue", "Overdue"
        CANCELLED = "cancelled", "Cancelled"

    participant = models.ForeignKey("participants.Participant", on_delete=models.CASCADE, related_name="visits")
    definition = models.ForeignKey(VisitDefinition, null=True, blank=True, on_delete=models.SET_NULL)
    study_site = models.ForeignKey("sites.StudySite", null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=120)
    scheduled_date = models.DateField()
    window_start = models.DateField(null=True, blank=True)
    window_end = models.DateField(null=True, blank=True)
    actual_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    missed_reason = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["scheduled_date"]


class VisitAssessment(StudyScopedModel):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name="assessments")
    name = models.CharField(max_length=140)
    form_code = models.CharField(max_length=40, blank=True)
    status = models.CharField(max_length=20, default="pending")
    completed_at = models.DateTimeField(null=True, blank=True)


class VisitProcedure(StudyScopedModel):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name="procedures")
    name = models.CharField(max_length=140)
    status = models.CharField(max_length=20, default="pending")
    notes = models.TextField(blank=True)


class VisitFollowUp(StudyScopedModel):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name="follow_ups")
    due_date = models.DateField()
    reason = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default="open")
    assigned_to = models.CharField(max_length=140, blank=True)
    notes = models.TextField(blank=True)
