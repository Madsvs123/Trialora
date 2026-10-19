from celery import shared_task
from django.utils import timezone

from apps.notifications.services import notify_members
from apps.safety.models import SeriousAdverseEvent


@shared_task
def escalate_unreported_saes():
    now = timezone.now()
    count = 0
    for sae in SeriousAdverseEvent.objects.filter(archived_at__isnull=True, adverse_event__status="open").select_related(
        "organization", "adverse_event"
    ):
        if sae.reported_to_sponsor_on:
            continue
        if sae.clock_start and (now - sae.clock_start).days >= sae.days_to_report:
            notify_members(
                sae.organization,
                "sae",
                f"SAE reporting clock exceeded: {sae.adverse_event.ae_number}",
                "Sponsor/regulator notification is overdue.",
                link="/app/safety",
                permission="safety.read",
            )
            count += 1
    return count
