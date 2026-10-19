from rest_framework.routers import DefaultRouter

from apps.participants.views import ParticipantViewSet, RandomizationViewSet, ScreeningViewSet, WithdrawalViewSet

router = DefaultRouter()
router.register("participants", ParticipantViewSet, basename="participants")
router.register("screenings", ScreeningViewSet, basename="screenings")
router.register("randomizations", RandomizationViewSet, basename="randomizations")
router.register("withdrawals", WithdrawalViewSet, basename="withdrawals")
urlpatterns = router.urls
