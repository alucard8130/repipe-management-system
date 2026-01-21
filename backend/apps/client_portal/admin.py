from django.contrib import admin
from .models import ClientUser, ProjectClientAccess, ProjectShareLink


@admin.register(ClientUser)
class ClientUserAdmin(admin.ModelAdmin):
    list_display = ("email", "customer", "company", "is_active", "language_preference")
    search_fields = ("email", "name")
    list_filter = ("company", "is_active")


@admin.register(ProjectClientAccess)
class ProjectClientAccessAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "customer",
        "client_user",
        "can_view_documents",
        "can_view_photos",
        "can_view_financials",
        "is_active",
    )
    list_filter = ("is_active",)


@admin.register(ProjectShareLink)
class ProjectShareLinkAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "expires_at",
        "revoked_at",
        "can_view_documents",
        "can_view_photos",
        "can_view_financials",
        "created_at",
    )
    list_filter = ("revoked_at",)
    readonly_fields = ("token_hash",)
