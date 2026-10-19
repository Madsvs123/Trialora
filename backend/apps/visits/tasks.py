from celery import shared_task
from django.utils import timezone

from apps.notifications.services import notify_members
from apps.visits.models import Visit


@shared_task
def flag_overdue_visits():
    today = timezone.now().date()
    overdue = Visit.objects.filter(
        archived_at__isnull=True,
        status__in=["scheduled", "in_window"],
        window_end__lt=today,
    )
    count = 0
    for visit in overdue.select_related("study", "organization"):
        visit.status = Visit.Status.OVERDUE
        visit.save(update_fields=["status", "updated_at"])
        notify_members(
            visit.organization,
            "overdue_visit",
            f"Overdue visit {visit.name}",
            f"Subject {visit.participant_id} visit is outside window.",
            link=f"/app/visits/{visit.id}",
            permission="visits.read",
        )
        count += 1
    return count
