from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.models import Membership
from apps.common.mixins import TenantQuerysetMixin
from apps.tenants.models import Country, Department, Organization, OrganizationSetting, Sponsor
from apps.tenants.serializers import (
    CountrySerializer,
    DepartmentSerializer,
    OrganizationSerializer,
    OrganizationSettingSerializer,
    SponsorSerializer,
)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]
    allow_unscoped = True
    search_fields = ["name", "legal_name"]
    filterset_fields = ["org_type", "is_active"]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Organization.objects.all()
        org_ids = Membership.objects.filter(user=user, is_active=True).values_list("organization_id", flat=True)
        return Organization.objects.filter(id__in=org_ids)

    @action(detail=False, methods=["get"])
    def current(self, request):
        org = getattr(request, "organization", None)
        if org is None:
            return Response({})
        return Response(self.get_serializer(org).data)


class DepartmentViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    search_fields = ["name", "code"]
    resource_name = "departments"


class SponsorViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    search_fields = ["name", "code", "contact_name"]
    resource_name = "sponsors"


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    allow_unscoped = True
    search_fields = ["name", "code"]
    pagination_class = None


class OrganizationSettingViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = OrganizationSetting.objects.all()
    serializer_class = OrganizationSettingSerializer
    resource_name = "settings"
    http_method_names = ["get", "put", "patch", "head", "options"]

    @action(detail=False, methods=["get", "patch"])
    def current(self, request):
        org = request.organization
        settings, _ = OrganizationSetting.objects.get_or_create(organization=org)
        if request.method == "PATCH":
            serializer = self.get_serializer(settings, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(self.get_serializer(settings).data)
