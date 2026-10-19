from rest_framework.routers import DefaultRouter

from apps.qualifications.views import CredentialViewSet, TrainingViewSet

router = DefaultRouter()
router.register("credentials", CredentialViewSet, basename="credentials")
router.register("trainings", TrainingViewSet, basename="trainings")
urlpatterns = router.urls
