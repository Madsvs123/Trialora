from apps.common.api import make_viewset
from apps.participants.models import Participant, RandomizationRecord, ScreeningRecord, Withdrawal
from apps.participants.serializers import (
    ParticipantSerializer,
    RandomizationRecordSerializer,
    ScreeningRecordSerializer,
    WithdrawalSerializer,
)

ParticipantViewSet = make_viewset(
    Participant,
    ParticipantSerializer,
    ["subject_id", "screening_number", "first_name", "last_name"],
    ["study", "status", "eligibility_status", "study_site"],
    "participants",
)
ScreeningViewSet = make_viewset(ScreeningRecord, ScreeningRecordSerializer, [], ["study", "result"], "screenings")
RandomizationViewSet = make_viewset(RandomizationRecord, RandomizationRecordSerializer, [], ["study"], "randomizations")
WithdrawalViewSet = make_viewset(Withdrawal, WithdrawalSerializer, ["reason"], ["study"], "withdrawals")
