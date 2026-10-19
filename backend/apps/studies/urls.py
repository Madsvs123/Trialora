from rest_framework.routers import DefaultRouter

from apps.studies.views import (
    CustomFieldViewSet,
    ProtocolViewSet,
    StatusWorkflowViewSet,
    StudyCountryViewSet,
    StudyMilestoneViewSet,
    StudyObjectiveViewSet,
    StudyTeamMemberViewSet,
    StudyTemplateViewSet,
    StudyViewSet,
)

router = DefaultRouter()
router.register("studies", StudyViewSet, basename="studies")
router.register("protocols", ProtocolViewSet, basename="protocols")
router.register("milestones", StudyMilestoneViewSet, basename="milestones")
router.register("objectives", StudyObjectiveViewSet, basename="objectives")
router.register("study-countries", StudyCountryViewSet, basename="study-countries")
router.register("study-teams", StudyTeamMemberViewSet, basename="study-teams")
router.register("templates", StudyTemplateViewSet, basename="templates")
router.register("custom-fields", CustomFieldViewSet, basename="custom-fields")
router.register("workflows", StatusWorkflowViewSet, basename="workflows")
urlpatterns = router.urls
