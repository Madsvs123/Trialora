from django.conf import settings
from rest_framework import serializers

from apps.common.api import make_serializer
from apps.participants.models import Participant, RandomizationRecord, ScreeningRecord, Withdrawal

PII_FIELDS = ("first_name", "last_name", "date_of_birth", "email", "phone", "address", "medical_record")


def can_view_pii(request, study_id):
    allowed = getattr(request, "can_view_pii_studies", set())
    return "*" in allowed or study_id in allowed


class ParticipantSerializer(serializers.ModelSerializer):
    study_code = serializers.CharField(source="study.code", read_only=True)
    site_name = serializers.CharField(source="study_site.site.name", read_only=True)
    pii_masked = serializers.SerializerMethodField()

    class Meta:
        model = Participant
        exclude = ("archived_at", "created_by", "updated_by")
        read_only_fields = ("id", "created_at", "updated_at")

    def get_pii_masked(self, obj):
        request = self.context.get("request")
        if request is None:
            return True
        return not can_view_pii(request, obj.study_id)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get("pii_masked"):
            for field in PII_FIELDS:
                if data.get(field):
                    data[field] = settings.PII_MASK
        return data


ScreeningRecordSerializer = make_serializer(ScreeningRecord)
RandomizationRecordSerializer = make_serializer(RandomizationRecord)
WithdrawalSerializer = make_serializer(Withdrawal)
