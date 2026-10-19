from django.contrib import admin

from apps.qualifications.models import StaffCredential, TrainingRecord

admin.site.register(StaffCredential)
admin.site.register(TrainingRecord)
