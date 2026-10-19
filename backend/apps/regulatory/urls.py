from rest_framework.routers import DefaultRouter

from apps.regulatory.views import ApprovalViewSet, EthicsCommitteeViewSet, RegulatoryObligationViewSet, SubmissionViewSet

router = DefaultRouter()
router.register("ethics-committees", EthicsCommitteeViewSet, basename="ethics-committees")
router.register("submissions", SubmissionViewSet, basename="submissions")
router.register("approvals", ApprovalViewSet, basename="approvals")
router.register("regulatory-obligations", RegulatoryObligationViewSet, basename="regulatory-obligations")
urlpatterns = router.urls
