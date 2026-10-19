from django.utils.deprecation import MiddlewareMixin

from apps.accounts.models import Membership, StudyAccess
from apps.tenants.models import Organization


class TenantIsolationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.organization = None
        request.membership = None
        request.allowed_study_ids = []
        request.study_access_map = {}
        request.can_view_pii_studies = set()

        user = getattr(request, "user", None)
        if user is None or not user.is_authenticated:
            return

        org_id = request.headers.get("X-Organization-Id") or request.GET.get("organization")
        organization = None
        if org_id:
            organization = Organization.objects.filter(id=org_id, is_active=True).first()
        elif getattr(user, "last_organization_id", None):
            organization = Organization.objects.filter(id=user.last_organization_id, is_active=True).first()

        if organization is None:
            membership = (
                Membership.objects.select_related("organization", "role")
                .filter(user=user, is_active=True, organization__is_active=True)
                .first()
            )
            if membership:
                organization = membership.organization
                request.membership = membership
        else:
            request.membership = (
                Membership.objects.select_related("role")
                .filter(user=user, organization=organization, is_active=True)
                .first()
            )

        request.organization = organization
        if organization and request.membership:
            accesses = list(
                StudyAccess.objects.filter(organization=organization, user=user, is_active=True).prefetch_related("sites")
            )
            request.allowed_study_ids = [a.study_id for a in accesses]
            request.study_access_map = {a.study_id: a for a in accesses}
            request.can_view_pii_studies = {a.study_id for a in accesses if a.can_view_pii}
            if request.membership.has_perm("participants.pii"):
                request.can_view_pii_studies.add("*")
            if user.last_organization_id != organization.id:
                user.last_organization = organization
                user.save(update_fields=["last_organization"])
