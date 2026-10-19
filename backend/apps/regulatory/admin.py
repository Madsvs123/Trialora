from django.contrib import admin

from apps.regulatory.models import Approval, EthicsCommittee, Submission

admin.site.register(EthicsCommittee)
admin.site.register(Submission)
admin.site.register(Approval)
