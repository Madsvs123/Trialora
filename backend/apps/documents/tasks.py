from celery import shared_task
from django.utils import timezone

from apps.documents.models import Document
from apps.notifications.services import notify_members
from apps.tenants.models import OrganizationSetting


@shared_task
def remind_expiring_documents():
    today = timezone.now().date()
    count = 0
    for document in Document.objects.filter(archived_at__isnull=True, expires_at__isnull=False).select_related("organization"):
        settings, _ = OrganizationSetting.objects.get_or_create(organization=document.organization)
        days = (document.expires_at - today).days
        if 0 <= days <= settings.document_expiry_days:
            notify_members(
                document.organization,
                "expiring_document",
                f"Document expiring: {document.title}",
                f"Expires in {days} day(s).",
                link="/app/documents",
                permission="documents.read",
            )
            count += 1
    return count
