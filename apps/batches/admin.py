from django.contrib import admin
from .models import BatchJob


@admin.register(BatchJob)
class BatchJobAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "status", "created_at")
    list_filter = ("status",)