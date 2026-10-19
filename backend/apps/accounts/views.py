from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import APIKey, InvestigatorProfile, Invitation, Membership, Role, StudyAccess
from apps.accounts.serializers import (
    AVAILABLE_PERMISSIONS,
    APIKeySerializer,
    AcceptInviteSerializer,
    InvitationSerializer,
    InvestigatorProfileSerializer,
    LoginSerializer,
    MembershipSerializer,
    RegisterSerializer,
    RoleSerializer,
    StudyAccessSerializer,
    UserSerializer,
)
from apps.accounts.services import (
    accept_invitation,
    login_user,
    register_organization,
    request_password_reset,
    reset_password,
    tokens_for,
)
from apps.common.mixins import TenantQuerysetMixin


class AuthThrottle(AnonRateThrottle):
    scope = "auth"


@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([AuthThrottle])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, organization = register_organization(serializer.validated_data)
    data = tokens_for(user)
    data["user"] = UserSerializer(user, context={"request": request}).data
    data["organizations"] = data["user"]["organizations"]
    data["organization_id"] = str(organization.id)
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([AuthThrottle])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = login_user(serializer.validated_data["email"], serializer.validated_data["password"])
    data = tokens_for(user)
    request.user = user
    data["user"] = UserSerializer(user, context={"request": request}).data
    data["organizations"] = data["user"]["organizations"]
    return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    refresh = request.data.get("refresh")
    if refresh:
        try:
            RefreshToken(refresh).blacklist()
        except Exception:
            pass
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def me_view(request):
    if request.method == "PATCH":
        serializer = UserSerializer(request.user, data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    return Response(UserSerializer(request.user, context={"request": request}).data)


@api_view(["POST"])
@permission_classes([AllowAny])
def accept_invite_view(request):
    serializer = AcceptInviteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, organization = accept_invitation(serializer.validated_data)
    data = tokens_for(user)
    data["user"] = UserSerializer(user, context={"request": request}).data
    data["organization_id"] = str(organization.id)
    return Response(data)


@api_view(["POST"])
@permission_classes([AllowAny])
def forgot_password_view(request):
    request_password_reset(request.data.get("email", ""))
    return Response({"detail": "If the account exists, a reset link was issued."})


@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password_view(request):
    reset_password(request.data.get("token", ""), request.data.get("password", ""))
    return Response({"detail": "Password updated."})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def permissions_catalog_view(request):
    return Response([{"code": p, "group": p.split(".")[0]} for p in AVAILABLE_PERMISSIONS])


class RoleViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    search_fields = ["name", "slug"]
    resource_name = "roles"


class MembershipViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = Membership.objects.select_related("user", "role")
    serializer_class = MembershipSerializer
    search_fields = ["user__email", "user__display_name", "title"]
    filterset_fields = ["role", "is_active"]
    resource_name = "members"


class InvitationViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = Invitation.objects.select_related("role")
    serializer_class = InvitationSerializer
    search_fields = ["email"]
    resource_name = "invitations"

    def perform_create(self, serializer):
        invitation = Invitation.issue(
            organization=self.request.organization,
            email=serializer.validated_data["email"],
            role=serializer.validated_data["role"],
            invited_by=self.request.user,
            message=serializer.validated_data.get("message", ""),
            is_investigator=serializer.validated_data.get("is_investigator", False),
        )
        serializer.instance = invitation


class StudyAccessViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = StudyAccess.objects.select_related("user", "study", "role")
    serializer_class = StudyAccessSerializer
    filterset_fields = ["study", "user", "is_active"]
    resource_name = "study-access"


class InvestigatorViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = InvestigatorProfile.objects.select_related("user")
    serializer_class = InvestigatorProfileSerializer
    search_fields = ["user__email", "user__display_name", "specialty", "institution"]
    resource_name = "investigators"


class APIKeyViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = APIKey.objects.all()
    serializer_class = APIKeySerializer
    resource_name = "api-keys"

    def create(self, request, *args, **kwargs):
        instance, raw = APIKey.issue(
            organization=request.organization,
            name=request.data.get("name", "API key"),
            created_by=request.user,
            scopes=request.data.get("scopes"),
        )
        data = self.get_serializer(instance).data
        data["key"] = raw
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def revoke(self, request, pk=None):
        from django.utils import timezone

        key = self.get_object()
        key.revoked_at = timezone.now()
        key.save(update_fields=["revoked_at"])
        return Response(self.get_serializer(key).data)
