import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trialora.settings")

app = Celery("trialora")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "flag-overdue-visits": {
        "task": "apps.visits.tasks.flag_overdue_visits",
        "schedule": crontab(minute=15),
    },
    "remind-expiring-documents": {
        "task": "apps.documents.tasks.remind_expiring_documents",
        "schedule": crontab(hour=6, minute=0),
    },
    "escalate-unresolved-findings": {
        "task": "apps.monitoring.tasks.escalate_unresolved_findings",
        "schedule": crontab(hour=7, minute=0),
    },
    "notify-enrollment-milestones": {
        "task": "apps.participants.tasks.notify_enrollment_milestones",
        "schedule": crontab(hour=8, minute=0),
    },
    "remind-training-and-credentials": {
        "task": "apps.qualifications.tasks.remind_expiring_credentials",
        "schedule": crontab(hour=6, minute=30),
    },
    "remind-monitoring-actions": {
        "task": "apps.monitoring.tasks.remind_open_actions",
        "schedule": crontab(hour=8, minute=30),
    },
    "refresh-site-metrics": {
        "task": "apps.sites.tasks.refresh_site_metrics",
        "schedule": crontab(minute=40),
    },
    "refresh-report-snapshots": {
        "task": "apps.reports.tasks.refresh_operational_snapshots",
        "schedule": crontab(minute=50),
    },
    "escalate-unreported-saes": {
        "task": "apps.safety.tasks.escalate_unreported_saes",
        "schedule": crontab(hour=7, minute=20),
    },
    "remind-expiring-approvals": {
        "task": "apps.regulatory.tasks.remind_expiring_approvals",
        "schedule": crontab(hour=6, minute=45),
    },
    "flag-low-kits": {
        "task": "apps.inventory.tasks.flag_low_and_expiring_kits",
        "schedule": crontab(hour=7, minute=40),
    },
}
