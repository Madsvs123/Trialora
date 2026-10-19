from celery import shared_task

from apps.notifications.services import notify_members
from apps.studies.models import Study


@shared_task
def notify_enrollment_milestones():
    for study in Study.objects.filter(archived_at__isnull=True, enrollment_target__gt=0):
        enrolled = study.participants_participants.filter(
            archived_at__isnull=True,
            status__in=["enrolled", "randomized", "active", "completed"],
        ).count()
        pct = round((enrolled / study.enrollment_target) * 100)
        if pct in (25, 50, 75, 100):
            notify_members(
                study.organization,
                "enrollment",
                f"{study.code} reached {pct}% enrollment",
                f"{enrolled} of {study.enrollment_target} participants enrolled.",
                link=f"/app/studies/{study.id}",
                permission="studies.read",
            )
    return "ok"
