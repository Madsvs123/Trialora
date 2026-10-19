from rest_framework import serializers

from apps.common.api import make_serializer
from apps.visits.models import Visit, VisitAssessment, VisitDefinition, VisitFollowUp, VisitProcedure

VisitDefinitionSerializer = make_serializer(VisitDefinition)
VisitSerializer = make_serializer(
    Visit,
    extra={
        "subject_id": serializers.CharField(source="participant.subject_id", read_only=True),
        "definition_code": serializers.CharField(source="definition.code", read_only=True, default=""),
    },
)
VisitAssessmentSerializer = make_serializer(VisitAssessment)
VisitProcedureSerializer = make_serializer(VisitProcedure)
VisitFollowUpSerializer = make_serializer(VisitFollowUp)
