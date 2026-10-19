from apps.common.api import make_viewset
from apps.sites.models import (
    FeasibilityAssessment,
    Site,
    SiteContact,
    SiteContract,
    SiteMetric,
    SiteQualification,
    StudySite,
)
from apps.sites.serializers import (
    FeasibilityAssessmentSerializer,
    SiteContactSerializer,
    SiteContractSerializer,
    SiteMetricSerializer,
    SiteQualificationSerializer,
    SiteSerializer,
    StudySiteSerializer,
)

SiteViewSet = make_viewset(Site, SiteSerializer, ["name", "institution", "city"], [], "sites")
StudySiteViewSet = make_viewset(StudySite, StudySiteSerializer, [], ["study", "status", "site"], "study-sites")
FeasibilityViewSet = make_viewset(FeasibilityAssessment, FeasibilityAssessmentSerializer, [], ["study", "status"], "feasibility")
SiteContractViewSet = make_viewset(SiteContract, SiteContractSerializer, ["title"], ["status"], "site-contracts")
SiteContactViewSet = make_viewset(SiteContact, SiteContactSerializer, ["name", "email"], ["site"], "site-contacts")
SiteQualificationViewSet = make_viewset(SiteQualification, SiteQualificationSerializer, ["kind"], ["site", "status"], "site-qualifications")
SiteMetricViewSet = make_viewset(SiteMetric, SiteMetricSerializer, [], ["study"], "site-metrics")
