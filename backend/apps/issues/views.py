from rest_framework import serializers

from apps.common.api import make_serializer, make_viewset
from apps.issues.models import CorrectiveAction, Escalation, Issue, ProtocolDeviation

IssueSerializer = make_serializer(
    Issue,
    extra={"owner_name": serializers.CharField(source="owner.label", read_only=True, default="")},
)
ProtocolDeviationSerializer = make_serializer(ProtocolDeviation)
CorrectiveActionSerializer = make_serializer(CorrectiveAction)
EscalationSerializer = make_serializer(Escalation)

IssueViewSet = make_viewset(Issue, IssueSerializer, ["title", "category"], ["study", "kind", "severity", "status"], "issues")
DeviationViewSet = make_viewset(ProtocolDeviation, ProtocolDeviationSerializer, [], ["study"], "deviations")
CorrectiveActionViewSet = make_viewset(CorrectiveAction, CorrectiveActionSerializer, [], ["status"], "corrective-actions")
EscalationViewSet = make_viewset(Escalation, EscalationSerializer, [], ["study"], "escalations")
