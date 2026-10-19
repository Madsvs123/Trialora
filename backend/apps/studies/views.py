from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.api import make_viewset
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
from apps.studies.serializers import (
    CustomFieldSerializer,
    ProtocolSerializer,
    StatusWorkflowSerializer,
    StudyCountrySerializer,
    StudyMilestoneSerializer,
    StudyObjectiveSerializer,
    StudySerializer,
    StudyTeamMemberSerializer,
    StudyTemplateSerializer,
)
from apps.studies.services import apply_template


class StudyViewSet(make_viewset(Study, StudySerializer, ["code", "title", "protocol_number", "indication"], ["status", "phase", "therapeutic_area"], "studies")):
    @action(detail=True, methods=["post"])
    def apply_template(self, request, pk=None):
        study = self.get_object()
        template = StudyTemplate.objects.filter(organization=request.organization, id=request.data.get("template")).first()
        if template is None:
            return Response({"detail": "Template not found."}, status=400)
        apply_template(study, template, request.user)
        return Response(self.get_serializer(study).data)


ProtocolViewSet = make_viewset(Protocol, ProtocolSerializer, ["title", "version"], ["study", "is_current"], "protocols")
StudyMilestoneViewSet = make_viewset(StudyMilestone, StudyMilestoneSerializer, ["name"], ["study", "status"], "milestones")
StudyObjectiveViewSet = make_viewset(StudyObjective, StudyObjectiveSerializer, ["text"], ["study", "kind"], "objectives")
StudyCountryViewSet = make_viewset(StudyCountry, StudyCountrySerializer, [], ["study"], "study-countries")
StudyTeamMemberViewSet = make_viewset(StudyTeamMember, StudyTeamMemberSerializer, ["role_label"], ["study"], "study-teams")
StudyTemplateViewSet = make_viewset(StudyTemplate, StudyTemplateSerializer, ["name"], ["is_active"], "templates")
CustomFieldViewSet = make_viewset(CustomField, CustomFieldSerializer, ["name", "field_key"], ["entity_type"], "custom-fields")
StatusWorkflowViewSet = make_viewset(StatusWorkflow, StatusWorkflowSerializer, ["name"], ["entity_type"], "workflows")
