from celery import shared_task
from django.utils import timezone

from apps.notifications.services import notify_members
from apps.regulatory.models import Approval, RegulatoryObligation
from apps.tenants.models import OrganizationSetting


@shared_task
def remind_expiring_approvals():
    today = timezone.now().date()
    count = 0
    for approval in Approval.objects.filter(archived_at__isnull=True, status="active", expires_on__isnull=False).select_related(
        "organization"
    ):
        settings, _ = OrganizationSetting.objects.get_or_create(organization=approval.organization)
        days = (approval.expires_on - today).days
        if 0 <= days <= settings.document_expiry_days:
            notify_members(
                approval.organization,
                "regulatory",
                f"Approval {approval.number} expires in {days} day(s)",
                link="/app/regulatory",
                permission="regulatory.read",
            )
            count += 1
    for item in RegulatoryObligation.objects.filter(archived_at__isnull=True, status="open", due_date__lte=today).select_related(
        "organization"
    ):
        notify_members(
            item.organization,
            "regulatory",
            f"Regulatory obligation due: {item.name}",
            link="/app/regulatory",
            permission="regulatory.read",
        )
        count += 1
    return count
