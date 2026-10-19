from django.db import models

from apps.common.models import StudyScopedModel


class Participant(StudyScopedModel):
    class Status(models.TextChoices):
        PRESCREEN = "prescreen", "Pre-screen"
        SCREENING = "screening", "Screening"
        SCREEN_FAILED = "screen_failed", "Screen failed"
        ENROLLED = "enrolled", "Enrolled"
        RANDOMIZED = "randomized", "Randomized"
        ACTIVE = "active", "Active"
        WITHDRAWN = "withdrawn", "Withdrawn"
        COMPLETED = "completed", "Completed"

    class Eligibility(models.TextChoices):
        UNKNOWN = "unknown", "Unknown"
        ELIGIBLE = "eligible", "Eligible"
        INELIGIBLE = "ineligible", "Ineligible"
        PENDING = "pending", "Pending review"

    study_site = models.ForeignKey("sites.StudySite", on_delete=models.CASCADE, related_name="participants")
    subject_id = models.CharField(max_length=40)
    screening_number = models.CharField(max_length=40, blank=True)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.PRESCREEN)
    eligibility_status = models.CharField(max_length=20, choices=Eligibility.choices, default=Eligibility.UNKNOWN)
    screened_on = models.DateField(null=True, blank=True)
    enrolled_on = models.DateField(null=True, blank=True)
    randomized_on = models.DateField(null=True, blank=True)
    completed_on = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=80, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    address = models.CharField(max_length=240, blank=True)
    medical_record = models.CharField(max_length=80, blank=True)
    notes = models.TextField(blank=True)
    custom_fields = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ("study", "subject_id")
        ordering = ["subject_id"]


class ScreeningRecord(StudyScopedModel):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="screenings")
    screened_on = models.DateField()
    result = models.CharField(max_length=24, default="pending")
    reason = models.TextField(blank=True)
    inclusion_met = models.BooleanField(default=False)
    exclusion_triggered = models.BooleanField(default=False)
    reviewer = models.CharField(max_length=140, blank=True)


class RandomizationRecord(StudyScopedModel):
    participant = models.OneToOneField(Participant, on_delete=models.CASCADE, related_name="randomization")
    arm = models.CharField(max_length=80)
    kit_number = models.CharField(max_length=40, blank=True)
    randomized_on = models.DateField()
    method = models.CharField(max_length=80, blank=True)
    stratum = models.CharField(max_length=80, blank=True)


class Withdrawal(StudyScopedModel):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="withdrawals")
    withdrawn_on = models.DateField()
    reason = models.CharField(max_length=160)
    category = models.CharField(max_length=40, default="subject")
    comments = models.TextField(blank=True)
    early_termination = models.BooleanField(default=True)
