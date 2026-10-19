from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.exports import csv_response
from apps.reports.services import dashboard_payload, enrollment_report, operational_report


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    resource_name = "dashboards"

    def get(self, request):
        return Response(dashboard_payload(request.organization))


class EnrollmentReportView(APIView):
    permission_classes = [IsAuthenticated]
    resource_name = "reports"

    def get(self, request):
        data = enrollment_report(request.organization, request.query_params.get("study"))
        if request.query_params.get("export") == "csv":
            rows = [
                [r.get("study__code"), r.get("study_site__site__name"), r.get("screened"), r.get("enrolled"), r.get("failed"), r.get("withdrawn"), r.get("completed")]
                for r in data["by_site"]
            ]
            return csv_response("enrollment.csv", ["study", "site", "screened", "enrolled", "failed", "withdrawn", "completed"], rows)
        return Response(data)


class OperationsReportView(APIView):
    permission_classes = [IsAuthenticated]
    resource_name = "reports"

    def get(self, request):
        return Response(operational_report(request.organization))
