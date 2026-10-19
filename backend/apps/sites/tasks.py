from celery import shared_task
from django.db.models import Count, Q
from django.utils import timezone

from apps.sites.models import SiteMetric, StudySite


@shared_task
def refresh_site_metrics():
    for study_site in StudySite.objects.select_related("study").all():
        participants = study_site.participants.alive() if hasattr(study_site.participants, "alive") else study_site.participants.all()
        metric, _ = SiteMetric.objects.get_or_create(
            organization=study_site.organization,
            study=study_site.study,
            study_site=study_site,
        )
        counts = participants.aggregate(
            screened=Count("id", filter=Q(status__in=["screening", "screen_failed", "enrolled", "randomized", "active", "withdrawn", "completed"])),
            enrolled=Count("id", filter=Q(status__in=["enrolled", "randomized", "active", "completed"])),
            screen_failed=Count("id", filter=Q(status="screen_failed")),
            withdrawn=Count("id", filter=Q(status="withdrawn")),
            completed=Count("id", filter=Q(status="completed")),
        )
        for key, value in counts.items():
            setattr(metric, key, value or 0)
        metric.open_findings = study_site.monitoring_visits.filter(findings__status="open").distinct().count()
        metric.deviations = study_site.issue_set.filter(kind="deviation", archived_at__isnull=True).count()
        if study_site.enrollment_target:
            metric.enrollment_pace = round((metric.enrolled / study_site.enrollment_target) * 100, 2)
        metric.last_refreshed = timezone.now()
        metric.save()
    return "ok"
