from rest_framework.routers import DefaultRouter

from apps.issues.views import CorrectiveActionViewSet, DeviationViewSet, EscalationViewSet, IssueViewSet

router = DefaultRouter()
router.register("issues", IssueViewSet, basename="issues")
router.register("deviations", DeviationViewSet, basename="deviations")
router.register("corrective-actions", CorrectiveActionViewSet, basename="corrective-actions")
router.register("escalations", EscalationViewSet, basename="escalations")
urlpatterns = router.urls
