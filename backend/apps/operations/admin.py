from django.contrib import admin
from .models import (
    WorkOrder,
    ChecklistTemplate,
    ChecklistTemplateItem,
    WorkOrderChecklistItem,
    TimeEntry,
    Permit,
    Inspection,
)

admin.site.register(WorkOrder)
admin.site.register(ChecklistTemplate)
admin.site.register(ChecklistTemplateItem)
admin.site.register(WorkOrderChecklistItem)
admin.site.register(TimeEntry)
admin.site.register(Permit)
admin.site.register(Inspection)

