from django.conf import settings
from django.db import models

from apps.common.models import StudyScopedModel, TenantModel


class Task(StudyScopedModel):
    class Priority(models.TextChoices):
        LOW = "low", "Low"
        NORMAL = "normal", "Normal"
        HIGH = "high", "High"
        URGENT = "urgent", "Urgent"

    study_site = models.ForeignKey("sites.StudySite", null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, default="open")
    priority = models.CharField(max_length=12, choices=Priority.choices, default=Priority.NORMAL)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_tasks")
    due_date = models.DateField(null=True, blank=True)
    milestone = models.ForeignKey("studies.StudyMilestone", null=True, blank=True, on_delete=models.SET_NULL)
    recurring = models.CharField(max_length=20, blank=True)
    workflow = models.CharField(max_length=80, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)


class TaskDependency(TenantModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="dependencies")
    depends_on = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="dependents")


class TaskComment(TenantModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
