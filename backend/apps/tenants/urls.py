from rest_framework.routers import DefaultRouter

from apps.tenants.views import (
    CountryViewSet,
    DepartmentViewSet,
    OrganizationSettingViewSet,
    OrganizationViewSet,
    SponsorViewSet,
)

router = DefaultRouter()
router.register("organizations", OrganizationViewSet, basename="organizations")
router.register("departments", DepartmentViewSet, basename="departments")
router.register("sponsors", SponsorViewSet, basename="sponsors")
router.register("countries", CountryViewSet, basename="countries")
router.register("settings", OrganizationSettingViewSet, basename="settings")

urlpatterns = router.urls
