from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.projects.models import Project
from .serializers import ProjectSerializer


class ProjectListAPIView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(company=user.company, is_active=True).order_by("id")


class ProjectDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(company=user.company, is_active=True).order_by("id")
