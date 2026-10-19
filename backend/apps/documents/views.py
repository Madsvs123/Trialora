from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.api import make_serializer, make_viewset
from apps.documents.models import Document, DocumentVersion

DocumentSerializer = make_serializer(Document)
DocumentVersionSerializer = make_serializer(DocumentVersion)


class DocumentViewSet(make_viewset(Document, DocumentSerializer, ["title"], ["category", "status", "study"], "documents")):
    @action(detail=True, methods=["post"])
    def upload_version(self, request, pk=None):
        document = self.get_object()
        version = (document.current_version or 1) + 1
        uploaded = request.FILES.get("file")
        record = DocumentVersion.objects.create(
            organization=request.organization,
            document=document,
            version=version,
            file=uploaded,
            file_name=getattr(uploaded, "name", request.data.get("file_name", "")),
            change_notes=request.data.get("change_notes", ""),
            uploaded_by=request.user,
            created_by=request.user,
        )
        document.current_version = version
        document.save(update_fields=["current_version", "updated_at"])
        return Response(DocumentVersionSerializer(record).data, status=status.HTTP_201_CREATED)


DocumentVersionViewSet = make_viewset(DocumentVersion, DocumentVersionSerializer, ["file_name"], ["document"], "document-versions")
