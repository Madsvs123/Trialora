from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.accounts.models import (
    APIKey,
    InvestigatorProfile,
    Invitation,
    Membership,
    Role,
    StudyAccess,
    User,
)
from apps.common.permissions import PERMISSIONS


class UserSerializer(serializers.ModelSerializer):
    organizations = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "display_name",
            "phone",
            "title",
            "avatar_color",
            "timezone",
            "is_investigator",
            "last_organization",
            "organizations",
            "permissions",
            "role",
        )
        read_only_fields = ("id", "email", "username")

    def get_organizations(self, obj):
        items = []
        for membership in obj.memberships.select_related("organization", "role").filter(is_active=True):
            items.append(
                {
                    "id": str(membership.organization_id),
                    "name": membership.organization.name,
                    "org_type": membership.organization.org_type,
                    "role": membership.role.slug,
                    "permissions": membership.role.permissions,
                }
            )
        return items

    def get_permissions(self, obj):
        membership = getattr(self.context.get("request"), "membership", None)
        return membership.role.permissions if membership else []

    def get_role(self, obj):
        membership = getattr(self.context.get("request"), "membership", None)
        return membership.role.slug if membership else None


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "name", "slug", "description", "is_system", "permissions", "created_at")
        read_only_fields = ("id", "is_system", "created_at")


class MembershipSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_name = serializers.CharField(source="user.label", read_only=True)
    role_name = serializers.CharField(source="role.name", read_only=True)

    class Meta:
        model = Membership
        fields = (
            "id",
            "user",
            "user_email",
            "user_name",
            "role",
            "role_name",
            "departments",
            "is_active",
            "title",
            "created_at",
        )
        read_only_fields = ("id", "created_at")


class InvitationSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source="role.name", read_only=True)
    is_open = serializers.BooleanField(read_only=True)

    class Meta:
        model = Invitation
        fields = (
            "id",
            "email",
            "role",
            "role_name",
            "message",
            "expires_at",
            "accepted_at",
            "is_investigator",
            "is_open",
            "token",
            "created_at",
        )
        read_only_fields = ("id", "expires_at", "accepted_at", "token", "created_at")


class StudyAccessSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.label", read_only=True)
    study_code = serializers.CharField(source="study.code", read_only=True)
    role_name = serializers.CharField(source="role.name", read_only=True)

    class Meta:
        model = StudyAccess
        fields = (
            "id",
            "user",
            "user_name",
            "study",
            "study_code",
            "role",
            "role_name",
            "sites",
            "can_view_pii",
            "is_active",
            "notes",
            "created_at",
        )
        read_only_fields = ("id", "created_at")


class InvestigatorProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.label", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = InvestigatorProfile
        fields = (
            "id",
            "user",
            "user_name",
            "email",
            "npi_number",
            "medical_license",
            "license_state",
            "specialty",
            "institution",
            "years_experience",
            "gcp_certified",
            "bio",
            "created_at",
        )
        read_only_fields = ("id", "created_at")


class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = ("id", "name", "prefix", "scopes", "last_used_at", "revoked_at", "created_at")
        read_only_fields = ("id", "prefix", "last_used_at", "revoked_at", "created_at")


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    display_name = serializers.CharField(required=False, allow_blank=True)
    organization_name = serializers.CharField()
    org_type = serializers.CharField(required=False, default="research")

    def validate_password(self, value):
        validate_password(value)
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class AcceptInviteSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    display_name = serializers.CharField(required=False, allow_blank=True)

    def validate_password(self, value):
        validate_password(value)
        return value


AVAILABLE_PERMISSIONS = PERMISSIONS
