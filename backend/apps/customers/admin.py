from django.contrib import admin
from .models import Customer, Property, Contact


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "customer_type", "company", "email", "phone", "is_active")
    search_fields = ("name", "company_name", "email")
    list_filter = ("customer_type", "company", "is_active")


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("address_line1", "city", "state", "zip_code", "property_type", "units_count", "company", "is_active")
    search_fields = ("address_line1", "city", "zip_code")
    list_filter = ("property_type", "state", "company", "is_active")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "role_title", "customer", "property", "email", "phone", "is_primary", "company", "is_active")
    search_fields = ("name", "email", "phone")
    list_filter = ("is_primary", "company", "is_active")
