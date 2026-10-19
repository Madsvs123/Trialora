from rest_framework import serializers

from apps.common.api import make_serializer
from apps.studies.models import (
    CustomField,
    Protocol,
    StatusWorkflow,
    Study,
    StudyCountry,
    StudyMilestone,
    StudyObjective,
    StudyTeamMember,
    StudyTemplate,
)

StudySerializer = make_serializer(
    Study,
    extra={
        "sponsor_name": serializers.CharField(source="sponsor.name", read_only=True, allow_null=True, default=""),
        "department_name": serializers.CharField(source="department.name", read_only=True, allow_null=True, default=""),
    },
)
ProtocolSerializer = make_serializer(Protocol)
StudyMilestoneSerializer = make_serializer(StudyMilestone)
StudyObjectiveSerializer = make_serializer(StudyObjective)
StudyCountrySerializer = make_serializer(
    StudyCountry,
    extra={"country_name": serializers.CharField(source="country.name", read_only=True)},
)
StudyTeamMemberSerializer = make_serializer(
    StudyTeamMember,
    extra={"user_name": serializers.CharField(source="user.label", read_only=True)},
)
StudyTemplateSerializer = make_serializer(StudyTemplate)
CustomFieldSerializer = make_serializer(CustomField)
StatusWorkflowSerializer = make_serializer(StatusWorkflow)
