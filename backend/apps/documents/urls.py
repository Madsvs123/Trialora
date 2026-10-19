from rest_framework.routers import DefaultRouter

from apps.documents.views import DocumentVersionViewSet, DocumentViewSet

router = DefaultRouter()
router.register("documents", DocumentViewSet, basename="documents")
router.register("document-versions", DocumentVersionViewSet, basename="document-versions")
urlpatterns = router.urls
