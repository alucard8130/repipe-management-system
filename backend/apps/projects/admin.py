from django.contrib import admin
from .models import (
    Project,
    ProjectScopeItem,
    Estimate,
    Contract,
    ProjectMilestone,
    ProjectMaterialEstimate,
    ProjectLaborRate,
)

admin.site.register(Project)
admin.site.register(ProjectScopeItem)
admin.site.register(Estimate)
admin.site.register(Contract)
admin.site.register(ProjectMilestone)
admin.site.register(ProjectMaterialEstimate)
admin.site.register(ProjectLaborRate)

from django.contrib import admin
from .models import Project, Milestone

class MilestoneInline(admin.TabularInline):
    model = Milestone
    extra = 0

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("project_number", "company", "status")
    list_filter = ("status", "company")
    inlines = [MilestoneInline]
