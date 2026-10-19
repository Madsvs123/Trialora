from django.db.models import Count, Q, Sum
from django.utils import timezone

from apps.documents.models import Document
from apps.finance.models import Payment, StudyBudget
from apps.inventory.models import Kit
from apps.issues.models import Issue
from apps.monitoring.models import Finding, MonitoringVisit
from apps.participants.models import Participant
from apps.regulatory.models import Approval
from apps.safety.models import AdverseEvent
from apps.sites.models import StudySite
from apps.studies.models import Study, StudyMilestone
from apps.visits.models import Visit


def dashboard_payload(organization):
    if organization is None:
        return {
            "studies": {"total": 0, "enrolling": 0, "active": 0, "by_status": [], "by_phase": []},
            "enrollment": {"target": 0, "screened": 0, "enrolled": 0, "screen_failed": 0, "active": 0, "withdrawn": 0, "completed": 0},
            "sites": {"total": 0, "active": 0, "activating": 0},
            "visits": {"scheduled": 0, "overdue": 0, "missed": 0, "completed": 0},
            "risks": {"open_issues": 0, "critical_issues": 0, "open_findings": 0, "expiring_documents": 0},
            "safety": {"aes": 0, "saes": 0, "open": 0},
            "regulatory": {"active_approvals": 0, "expiring": 0},
            "inventory": {"available_kits": 0, "quarantine": 0},
        }
    studies = Study.objects.filter(organization=organization, archived_at__isnull=True)
    participants = Participant.objects.filter(organization=organization, archived_at__isnull=True)
    sites = StudySite.objects.filter(organization=organization, archived_at__isnull=True)
    visits = Visit.objects.filter(organization=organization, archived_at__isnull=True)
    issues = Issue.objects.filter(organization=organization, archived_at__isnull=True)
    findings = Finding.objects.filter(organization=organization, archived_at__isnull=True)
    documents = Document.objects.filter(organization=organization, archived_at__isnull=True)
    aes = AdverseEvent.objects.filter(organization=organization, archived_at__isnull=True)
    kits = Kit.objects.filter(organization=organization, archived_at__isnull=True)
    approvals = Approval.objects.filter(organization=organization, archived_at__isnull=True)
    enrolled = participants.filter(status__in=["enrolled", "randomized", "active", "completed"])
    return {
        "studies": {
            "total": studies.count(),
            "enrolling": studies.filter(status="enrolling").count(),
            "active": studies.filter(status__in=["active", "enrolling"]).count(),
            "by_status": list(studies.values("status").annotate(count=Count("id"))),
            "by_phase": list(studies.values("phase").annotate(count=Count("id"))),
        },
        "enrollment": {
            "target": studies.aggregate(total=Sum("enrollment_target"))["total"] or 0,
            "screened": participants.exclude(status="prescreen").count(),
            "enrolled": enrolled.count(),
            "screen_failed": participants.filter(status="screen_failed").count(),
            "active": participants.filter(status__in=["enrolled", "randomized", "active"]).count(),
            "withdrawn": participants.filter(status="withdrawn").count(),
            "completed": participants.filter(status="completed").count(),
        },
        "sites": {
            "total": sites.count(),
            "active": sites.filter(status__in=["active", "enrolling"]).count(),
            "activating": sites.filter(status="activating").count(),
        },
        "visits": {
            "scheduled": visits.filter(status="scheduled").count(),
            "overdue": visits.filter(status="overdue").count(),
            "missed": visits.filter(status="missed").count(),
            "completed": visits.filter(status="completed").count(),
        },
        "risks": {
            "open_issues": issues.filter(status="open").count(),
            "critical_issues": issues.filter(status="open", severity="critical").count(),
            "open_findings": findings.filter(status="open").count(),
            "expiring_documents": documents.filter(expires_at__isnull=False, expires_at__lte=timezone.now().date()).count(),
        },
        "safety": {
            "aes": aes.count(),
            "saes": aes.filter(seriousness="serious").count(),
            "open": aes.filter(status="open").count(),
        },
        "regulatory": {
            "active_approvals": approvals.filter(status="active").count(),
            "expiring": approvals.filter(status="active", expires_on__isnull=False, expires_on__lte=timezone.now().date()).count(),
        },
        "inventory": {
            "available_kits": kits.filter(status="available").count(),
            "quarantine": kits.filter(status="quarantine").count(),
        },
    }


def enrollment_report(organization, study_id=None):
    if organization is None:
        return {"totals": {"screened": 0, "enrolled": 0, "screen_failed": 0, "active": 0, "withdrawn": 0, "completed": 0, "target": 0}, "by_site": [], "by_status": []}
    participants = Participant.objects.filter(organization=organization, archived_at__isnull=True)
    sites = StudySite.objects.filter(organization=organization, archived_at__isnull=True)
    if study_id:
        participants = participants.filter(study_id=study_id)
        sites = sites.filter(study_id=study_id)
    by_site = list(
        participants.values("study_site__site__name", "study__code")
        .annotate(
            screened=Count("id", filter=~Q(status="prescreen")),
            enrolled=Count("id", filter=Q(status__in=["enrolled", "randomized", "active", "completed"])),
            failed=Count("id", filter=Q(status="screen_failed")),
            withdrawn=Count("id", filter=Q(status="withdrawn")),
            completed=Count("id", filter=Q(status="completed")),
        )
        .order_by("study__code")
    )
    return {
        "totals": {
            "screened": participants.exclude(status="prescreen").count(),
            "enrolled": participants.filter(status__in=["enrolled", "randomized", "active", "completed"]).count(),
            "screen_failed": participants.filter(status="screen_failed").count(),
            "active": participants.filter(status__in=["enrolled", "randomized", "active"]).count(),
            "withdrawn": participants.filter(status="withdrawn").count(),
            "completed": participants.filter(status="completed").count(),
            "target": sites.aggregate(total=Sum("enrollment_target"))["total"] or 0,
        },
        "by_site": by_site,
        "by_status": list(participants.values("status").annotate(count=Count("id"))),
    }


def operational_report(organization):
    if organization is None:
        return {"milestones": [], "monitoring": [], "budgets": [], "payments": [], "document_completeness": {"total": 0, "current": 0}, "safety": [], "inventory": []}
    return {
        "milestones": list(
            StudyMilestone.objects.filter(organization=organization, archived_at__isnull=True).values("status").annotate(count=Count("id"))
        ),
        "monitoring": list(
            MonitoringVisit.objects.filter(organization=organization, archived_at__isnull=True).values("status").annotate(count=Count("id"))
        ),
        "budgets": list(
            StudyBudget.objects.filter(organization=organization, archived_at__isnull=True).values("study__code").annotate(planned=Sum("planned"), actual=Sum("actual"))
        ),
        "payments": list(
            Payment.objects.filter(organization=organization, archived_at__isnull=True).values("status").annotate(count=Count("id"), amount=Sum("amount"))
        ),
        "document_completeness": {
            "total": Document.objects.filter(organization=organization, archived_at__isnull=True).count(),
            "current": Document.objects.filter(organization=organization, archived_at__isnull=True, status="current").count(),
        },
        "safety": list(AdverseEvent.objects.filter(organization=organization, archived_at__isnull=True).values("seriousness").annotate(count=Count("id"))),
        "inventory": list(Kit.objects.filter(organization=organization, archived_at__isnull=True).values("status").annotate(count=Count("id"))),
    }
