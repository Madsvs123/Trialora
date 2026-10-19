from django.contrib import admin

from apps.visits.models import Visit, VisitDefinition

admin.site.register(VisitDefinition)
admin.site.register(Visit)
