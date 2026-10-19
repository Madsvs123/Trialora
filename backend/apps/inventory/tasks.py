from celery import shared_task
from django.utils import timezone

from apps.inventory.models import Kit
from apps.notifications.services import notify_members


@shared_task
def flag_low_and_expiring_kits():
    today = timezone.now().date()
    count = 0
    studies = {}
    for kit in Kit.objects.filter(archived_at__isnull=True, status="available").select_related("organization", "study"):
        studies.setdefault((kit.organization_id, kit.study_id), {"org": kit.organization, "available": 0, "expiring": 0})
        studies[(kit.organization_id, kit.study_id)]["available"] += 1
        if kit.expiry_date and 0 <= (kit.expiry_date - today).days <= 30:
            studies[(kit.organization_id, kit.study_id)]["expiring"] += 1
    for payload in studies.values():
        if payload["available"] < 8 or payload["expiring"]:
            notify_members(
                payload["org"],
                "inventory",
                "Investigational product attention required",
                f"{payload['available']} kits available, {payload['expiring']} expiring within 30 days.",
                link="/app/inventory",
                permission="inventory.read",
            )
            count += 1
    return count
