from rest_framework.routers import DefaultRouter

from apps.monitoring.views import (
    ActionItemViewSet,
    FindingViewSet,
    FollowUpLetterViewSet,
    MonitoringVisitViewSet,
    RiskIndicatorViewSet,
    TripReportViewSet,
)

router = DefaultRouter()
router.register("monitoring-visits", MonitoringVisitViewSet, basename="monitoring-visits")
router.register("trip-reports", TripReportViewSet, basename="trip-reports")
router.register("findings", FindingViewSet, basename="findings")
router.register("action-items", ActionItemViewSet, basename="action-items")
router.register("follow-up-letters", FollowUpLetterViewSet, basename="follow-up-letters")
router.register("risk-indicators", RiskIndicatorViewSet, basename="risk-indicators")
urlpatterns = router.urls
