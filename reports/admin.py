from django.contrib import admin
from .models import Reports, ReportImage


class ReportImageInline(admin.TabularInline):
    model = ReportImage


@admin.register(Reports)
class ReportsAdmin(admin.ModelAdmin):
    list_display = ('user', 'program', 'posted_at')
    prepopulated_fields = {'slug': ('body',)}
    inlines = [ReportImageInline]
