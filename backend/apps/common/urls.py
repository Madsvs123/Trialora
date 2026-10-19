from django.urls import include, path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def health(_request):
    return Response({"status": "ok", "service": "trialora"})


urlpatterns = [
    path("health/", health),
    path("", include("apps.accounts.urls")),
    path("", include("apps.tenants.urls")),
    path("", include("apps.studies.urls")),
    path("", include("apps.sites.urls")),
    path("", include("apps.participants.urls")),
    path("", include("apps.visits.urls")),
    path("", include("apps.monitoring.urls")),
    path("", include("apps.issues.urls")),
    path("", include("apps.documents.urls")),
    path("", include("apps.qualifications.urls")),
    path("", include("apps.workitems.urls")),
    path("", include("apps.finance.urls")),
    path("", include("apps.notifications.urls")),
    path("", include("apps.audit.urls")),
    path("", include("apps.search.urls")),
    path("", include("apps.reports.urls")),
    path("", include("apps.safety.urls")),
    path("", include("apps.regulatory.urls")),
    path("", include("apps.inventory.urls")),
]
