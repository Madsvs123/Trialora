from celery import shared_task
from django.utils import timezone

from apps.notifications.services import notify_user
from apps.qualifications.models import StaffCredential, TrainingRecord


@shared_task
def remind_expiring_credentials():
    today = timezone.now().date()
    count = 0
    for cred in StaffCredential.objects.filter(archived_at__isnull=True, expires_on__isnull=False).select_related("organization", "user"):
        days = (cred.expires_on - today).days
        if 0 <= days <= 30:
            notify_user(cred.organization, cred.user, "training", f"{cred.name} expires in {days} day(s)", link="/app/staff")
            count += 1
    for training in TrainingRecord.objects.filter(archived_at__isnull=True, status="assigned", due_date__isnull=False).select_related("organization", "user"):
        if training.due_date <= today:
            notify_user(training.organization, training.user, "training", f"Training due: {training.course}", link="/app/staff")
            count += 1
    return count
