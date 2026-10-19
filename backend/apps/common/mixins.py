from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from apps.audit.services import log_action


class TenantQuerysetMixin:
    org_field = "organization"
    study_field = "study"
    apply_study_scope = True

    def get_organization(self):
        org = getattr(self.request, "organization", None)
        if org is None and not getattr(self, "allow_unscoped", False):
            raise PermissionDenied("Organization context required (X-Organization-Id).")
        return org

    def get_queryset(self):
        qs = super().get_queryset()
        org = getattr(self.request, "organization", None)
        if org is None:
            return qs if getattr(self, "allow_unscoped", False) else qs.none()
        if hasattr(qs.model, self.org_field):
            qs = qs.filter(**{self.org_field: org})
        if hasattr(qs.model, "archived_at") and self.request.query_params.get("include_archived") != "true":
            qs = qs.filter(archived_at__isnull=True)
        qs = self._apply_study_scope(qs)
        return qs

    def _apply_study_scope(self, qs):
        if not self.apply_study_scope or not hasattr(qs.model, self.study_field):
            return qs
        allowed = getattr(self.request, "allowed_study_ids", None)
        if allowed:
            return qs.filter(**{f"{self.study_field}_id__in": allowed})
        return qs

    def perform_create(self, serializer):
        org = getattr(self.request, "organization", None)
        if org is None and not getattr(self, "allow_unscoped", False):
            raise ValidationError({"organization": "Organization context required."})
        extras = {}
        model = serializer.Meta.model
        if org is not None and hasattr(model, "organization"):
            extras["organization"] = org
        if hasattr(model, "created_by"):
            extras["created_by"] = self.request.user
        if hasattr(model, "updated_by"):
            extras["updated_by"] = self.request.user
        serializer.save(**extras)
        log_action(
            request=self.request,
            action="create",
            resource_type=model.__name__,
            resource_id=str(serializer.instance.pk),
            message=f"Created {model.__name__}",
        )

    def perform_update(self, serializer):
        extras = {}
        model = serializer.Meta.model
        if hasattr(model, "updated_by"):
            extras["updated_by"] = self.request.user
        serializer.save(**extras)
        log_action(
            request=self.request,
            action="update",
            resource_type=model.__name__,
            resource_id=str(serializer.instance.pk),
            message=f"Updated {model.__name__}",
        )

    def perform_destroy(self, instance):
        resource_type = instance.__class__.__name__
        resource_id = str(instance.pk)
        if hasattr(instance, "archive"):
            instance.archive()
        else:
            instance.delete()
        log_action(
            request=self.request,
            action="delete",
            resource_type=resource_type,
            resource_id=resource_id,
            message=f"Archived {resource_type}",
        )


class ArchiveMixin:
    @action(detail=True, methods=["post"])
    def archive(self, request, pk=None):
        instance = self.get_object()
        instance.archive()
        return Response(status=status.HTTP_204_NO_CONTENT)
