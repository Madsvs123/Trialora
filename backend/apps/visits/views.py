from apps.common.api import make_viewset
from apps.visits.models import Visit, VisitAssessment, VisitDefinition, VisitFollowUp, VisitProcedure
from apps.visits.serializers import (
    VisitAssessmentSerializer,
    VisitDefinitionSerializer,
    VisitFollowUpSerializer,
    VisitProcedureSerializer,
    VisitSerializer,
)

VisitDefinitionViewSet = make_viewset(VisitDefinition, VisitDefinitionSerializer, ["name", "code"], ["study"], "visit-definitions")
VisitViewSet = make_viewset(Visit, VisitSerializer, ["name", "participant__subject_id"], ["study", "status", "participant"], "visits")
VisitAssessmentViewSet = make_viewset(VisitAssessment, VisitAssessmentSerializer, ["name"], ["status"], "assessments")
VisitProcedureViewSet = make_viewset(VisitProcedure, VisitProcedureSerializer, ["name"], ["status"], "procedures")
VisitFollowUpViewSet = make_viewset(VisitFollowUp, VisitFollowUpSerializer, ["reason"], ["status"], "follow-ups")
