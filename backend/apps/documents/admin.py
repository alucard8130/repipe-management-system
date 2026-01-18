from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "file_name",
        "category",
        "project",
        "visible_to_client",
        "file_size",
        "company",
        "created_at",
    )
    list_filter = ("category", "visible_to_client", "company")
    search_fields = ("file_name",)
