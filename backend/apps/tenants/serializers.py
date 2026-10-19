from rest_framework import serializers

from apps.tenants.models import Country, Department, Organization, OrganizationSetting, Sponsor


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "slug",
            "org_type",
            "legal_name",
            "country",
            "timezone",
            "logo_color",
            "website",
            "is_active",
            "settings",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "slug", "created_at", "updated_at")


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("id", "name", "code", "description", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = (
            "id",
            "name",
            "code",
            "contact_name",
            "contact_email",
            "country",
            "notes",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "code", "name", "region")


class OrganizationSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationSetting
        exclude = ("organization", "archived_at", "created_by", "updated_by")
        read_only_fields = ("id", "created_at", "updated_at")
