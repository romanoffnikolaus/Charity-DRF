from django.contrib import admin

from .models import ReportRating, ProgramRating, ProgramComment

admin.site.register(ReportRating)
admin.site.register(ProgramRating)
admin.site.register(ProgramComment)
