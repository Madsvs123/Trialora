from rest_framework.routers import DefaultRouter

from apps.sites.views import (
    FeasibilityViewSet,
    SiteContactViewSet,
    SiteContractViewSet,
    SiteMetricViewSet,
    SiteQualificationViewSet,
    SiteViewSet,
    StudySiteViewSet,
)

router = DefaultRouter()
router.register("sites", SiteViewSet, basename="sites")
router.register("study-sites", StudySiteViewSet, basename="study-sites")
router.register("feasibility", FeasibilityViewSet, basename="feasibility")
router.register("site-contracts", SiteContractViewSet, basename="site-contracts")
router.register("site-contacts", SiteContactViewSet, basename="site-contacts")
router.register("site-qualifications", SiteQualificationViewSet, basename="site-qualifications")
router.register("site-metrics", SiteMetricViewSet, basename="site-metrics")
urlpatterns = router.urls
