from rest_framework.routers import DefaultRouter

from apps.safety.views import AdverseEventViewSet, SafetyReportViewSet, SafetySignalViewSet, SeriousAdverseEventViewSet

router = DefaultRouter()
router.register("adverse-events", AdverseEventViewSet, basename="adverse-events")
router.register("saes", SeriousAdverseEventViewSet, basename="saes")
router.register("safety-reports", SafetyReportViewSet, basename="safety-reports")
router.register("safety-signals", SafetySignalViewSet, basename="safety-signals")
urlpatterns = router.urls
