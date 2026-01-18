from django.urls import path
from .views import ProjectListAPIView, ProjectDetailAPIView

urlpatterns = [
    path("", ProjectListAPIView.as_view(), name="project-list"),
    path("<int:pk>/", ProjectDetailAPIView.as_view(), name="project-detail"),
]
