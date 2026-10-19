from django.urls import path

from apps.reports.views import DashboardView, EnrollmentReportView, OperationsReportView

urlpatterns = [
    path("dashboards/overview/", DashboardView.as_view()),
    path("reports/enrollment/", EnrollmentReportView.as_view()),
    path("reports/operations/", OperationsReportView.as_view()),
]
