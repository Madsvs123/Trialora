from rest_framework import serializers

from apps.common.api import make_serializer, make_viewset
from apps.qualifications.models import StaffCredential, TrainingRecord

StaffCredentialSerializer = make_serializer(
    StaffCredential,
    extra={"user_name": serializers.CharField(source="user.label", read_only=True)},
)
TrainingRecordSerializer = make_serializer(
    TrainingRecord,
    extra={"user_name": serializers.CharField(source="user.label", read_only=True)},
)

CredentialViewSet = make_viewset(StaffCredential, StaffCredentialSerializer, ["name", "issuer"], ["kind", "status"], "credentials")
TrainingViewSet = make_viewset(TrainingRecord, TrainingRecordSerializer, ["course"], ["status", "study"], "trainings")
