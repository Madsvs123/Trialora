from django.contrib import admin

from apps.monitoring.models import Finding, MonitoringVisit

admin.site.register(MonitoringVisit)
admin.site.register(Finding)
