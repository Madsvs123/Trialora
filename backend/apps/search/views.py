from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.documents.models import Document
from apps.inventory.models import Kit
from apps.issues.models import Issue
from apps.participants.models import Participant
from apps.regulatory.models import Submission
from apps.safety.models import AdverseEvent
from apps.sites.models import Site
from apps.studies.models import Study


class GlobalSearchView(APIView):
    permission_classes = [IsAuthenticated]
    resource_name = "search"

    def get(self, request):
        q = (request.query_params.get("q") or "").strip()
        org = request.organization
        if not q or org is None:
            return Response({"results": []})
        results = []
        studies = list(Study.objects.filter(organization=org, archived_at__isnull=True, title__icontains=q)[:6])
        if not studies:
            studies = list(Study.objects.filter(organization=org, archived_at__isnull=True, code__icontains=q)[:6])
        for item in studies:
            results.append({"type": "study", "id": str(item.id), "title": item.title, "subtitle": item.code})
        for item in Site.objects.filter(organization=org, archived_at__isnull=True, name__icontains=q)[:6]:
            results.append({"type": "site", "id": str(item.id), "title": item.name, "subtitle": item.institution})
        for item in Participant.objects.filter(organization=org, archived_at__isnull=True, subject_id__icontains=q)[:6]:
            results.append({"type": "participant", "id": str(item.id), "title": item.subject_id, "subtitle": item.status})
        for item in Issue.objects.filter(organization=org, archived_at__isnull=True, title__icontains=q)[:6]:
            results.append({"type": "issue", "id": str(item.id), "title": item.title, "subtitle": item.severity})
        for item in Document.objects.filter(organization=org, archived_at__isnull=True, title__icontains=q)[:6]:
            results.append({"type": "document", "id": str(item.id), "title": item.title, "subtitle": item.category})
        for item in AdverseEvent.objects.filter(organization=org, archived_at__isnull=True, term__icontains=q)[:6]:
            results.append({"type": "safety", "id": str(item.id), "title": item.term, "subtitle": item.ae_number})
        for item in Submission.objects.filter(organization=org, archived_at__isnull=True, title__icontains=q)[:6]:
            results.append({"type": "regulatory", "id": str(item.id), "title": item.title, "subtitle": item.status})
        for item in Kit.objects.filter(organization=org, archived_at__isnull=True, kit_number__icontains=q)[:6]:
            results.append({"type": "inventory", "id": str(item.id), "title": item.kit_number, "subtitle": item.status})
        return Response({"results": results, "query": q})
