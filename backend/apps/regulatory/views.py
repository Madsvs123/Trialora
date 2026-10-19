from rest_framework import serializers

from apps.common.api import make_serializer, make_viewset
from apps.regulatory.models import Approval, EthicsCommittee, RegulatoryObligation, Submission

EthicsCommitteeSerializer = make_serializer(EthicsCommittee)
SubmissionSerializer = make_serializer(
    Submission,
    extra={"committee_name": serializers.CharField(source="committee.name", read_only=True, allow_null=True, default="")},
)
ApprovalSerializer = make_serializer(Approval)
RegulatoryObligationSerializer = make_serializer(RegulatoryObligation)

EthicsCommitteeViewSet = make_viewset(EthicsCommittee, EthicsCommitteeSerializer, ["name", "city"], ["kind"], "ethics-committees")
SubmissionViewSet = make_viewset(Submission, SubmissionSerializer, ["title", "reference"], ["study", "kind", "status"], "submissions")
ApprovalViewSet = make_viewset(Approval, ApprovalSerializer, ["number"], ["study", "status"], "approvals")
RegulatoryObligationViewSet = make_viewset(
    RegulatoryObligation, RegulatoryObligationSerializer, ["name", "authority"], ["status"], "regulatory-obligations"
)
