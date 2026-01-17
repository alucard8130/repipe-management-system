from django.contrib import admin
from .models import User, Role, UserRole


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "company", "is_active", "language_preference")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("company", "is_active", "language_preference")


admin.site.register(Role)
admin.site.register(UserRole)
