from rest_framework import serializers

from apps.common.api import make_serializer, make_viewset
from apps.monitoring.models import ActionItem, Finding, FollowUpLetter, MonitoringVisit, RiskIndicator, TripReport

MonitoringVisitSerializer = make_serializer(
    MonitoringVisit,
    extra={"monitor_name": serializers.CharField(source="monitor.label", read_only=True, default="")},
)
TripReportSerializer = make_serializer(TripReport)
FindingSerializer = make_serializer(Finding)
ActionItemSerializer = make_serializer(ActionItem)
FollowUpLetterSerializer = make_serializer(FollowUpLetter)
RiskIndicatorSerializer = make_serializer(RiskIndicator)

MonitoringVisitViewSet = make_viewset(MonitoringVisit, MonitoringVisitSerializer, [], ["study", "status", "kind"], "monitoring-visits")
TripReportViewSet = make_viewset(TripReport, TripReportSerializer, ["summary"], ["status"], "trip-reports")
FindingViewSet = make_viewset(Finding, FindingSerializer, ["title"], ["severity", "status"], "findings")
ActionItemViewSet = make_viewset(ActionItem, ActionItemSerializer, ["title"], ["status"], "action-items")
FollowUpLetterViewSet = make_viewset(FollowUpLetter, FollowUpLetterSerializer, ["subject"], [], "follow-up-letters")
RiskIndicatorViewSet = make_viewset(RiskIndicator, RiskIndicatorSerializer, ["name"], ["study"], "risk-indicators")
