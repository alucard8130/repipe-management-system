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
