from rest_framework import serializers

from apps.common.api import make_serializer
from apps.sites.models import (
    FeasibilityAssessment,
    Site,
    SiteContact,
    SiteContract,
    SiteMetric,
    SiteQualification,
    StudySite,
)

SiteSerializer = make_serializer(
    Site,
    extra={
        "country_name": serializers.CharField(source="country.name", read_only=True, allow_null=True, default=""),
        "pi_name": serializers.CharField(source="principal_investigator.label", read_only=True, allow_null=True, default=""),
    },
)
StudySiteSerializer = make_serializer(
    StudySite,
    extra={
        "site_name": serializers.CharField(source="site.name", read_only=True),
        "study_code": serializers.CharField(source="study.code", read_only=True),
        "investigator_name": serializers.CharField(source="investigator.label", read_only=True, allow_null=True, default=""),
    },
)
FeasibilityAssessmentSerializer = make_serializer(FeasibilityAssessment)
SiteContractSerializer = make_serializer(SiteContract)
SiteContactSerializer = make_serializer(SiteContact)
SiteQualificationSerializer = make_serializer(SiteQualification)
SiteMetricSerializer = make_serializer(SiteMetric)
