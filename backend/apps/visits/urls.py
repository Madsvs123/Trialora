from rest_framework.routers import DefaultRouter

from apps.visits.views import (
    VisitAssessmentViewSet,
    VisitDefinitionViewSet,
    VisitFollowUpViewSet,
    VisitProcedureViewSet,
    VisitViewSet,
)

router = DefaultRouter()
router.register("visit-definitions", VisitDefinitionViewSet, basename="visit-definitions")
router.register("visits", VisitViewSet, basename="visits")
router.register("assessments", VisitAssessmentViewSet, basename="assessments")
router.register("procedures", VisitProcedureViewSet, basename="procedures")
router.register("follow-ups", VisitFollowUpViewSet, basename="follow-ups")
urlpatterns = router.urls
