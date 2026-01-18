from rest_framework import serializers
from apps.projects.models import Project
from apps.services.project_cost_service import ProjectCostService


class ProjectSerializer(serializers.ModelSerializer):
    cost_summary = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "project_number",
            "title",
            "status",
            "estimated_start_date",
            "estimated_end_date",
            "actual_start_date",
            "actual_end_date",
            "cost_summary",
        ]

    def get_cost_summary(self, obj):
        return ProjectCostService.get_profit_summary(obj)
