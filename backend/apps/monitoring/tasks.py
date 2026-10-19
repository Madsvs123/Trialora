from celery import shared_task
from django.utils import timezone

from apps.monitoring.models import ActionItem, Finding
from apps.notifications.services import notify_members, notify_user


@shared_task
def escalate_unresolved_findings():
    today = timezone.now().date()
    count = 0
    for finding in Finding.objects.filter(archived_at__isnull=True, status="open", due_date__lt=today).select_related("organization"):
        notify_members(
            finding.organization,
            "unresolved_finding",
            f"Overdue finding: {finding.title}",
            f"{finding.severity} finding is past due.",
            link=f"/app/monitoring",
            permission="monitoring.read",
        )
        count += 1
    return count


@shared_task
def remind_open_actions():
    today = timezone.now().date()
    count = 0
    for item in ActionItem.objects.filter(archived_at__isnull=True, status="open", due_date__lte=today).select_related("organization", "owner"):
        if item.owner:
            notify_user(
                item.organization,
                item.owner,
                "monitoring_action",
                f"Action due: {item.title}",
                link="/app/monitoring",
            )
        count += 1
    return count
