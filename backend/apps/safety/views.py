from rest_framework import serializers

from apps.common.api import make_serializer, make_viewset
from apps.safety.models import AdverseEvent, SafetyReport, SafetySignal, SeriousAdverseEvent

AdverseEventSerializer = make_serializer(
    AdverseEvent,
    extra={
        "subject_id": serializers.CharField(source="participant.subject_id", read_only=True),
        "reporter_name": serializers.CharField(source="reporter.label", read_only=True, allow_null=True, default=""),
    },
)
SeriousAdverseEventSerializer = make_serializer(SeriousAdverseEvent)
SafetyReportSerializer = make_serializer(SafetyReport)
SafetySignalSerializer = make_serializer(SafetySignal)

AdverseEventViewSet = make_viewset(
    AdverseEvent,
    AdverseEventSerializer,
    ["ae_number", "term", "participant__subject_id"],
    ["study", "seriousness", "severity", "status", "causality"],
    "adverse-events",
)
SeriousAdverseEventViewSet = make_viewset(SeriousAdverseEvent, SeriousAdverseEventSerializer, [], ["study", "is_susar"], "saes")
SafetyReportViewSet = make_viewset(SafetyReport, SafetyReportSerializer, ["destination", "reference"], ["status", "report_type"], "safety-reports")
SafetySignalViewSet = make_viewset(SafetySignal, SafetySignalSerializer, ["name", "term"], ["status"], "safety-signals")
