from django.urls import path, include

urlpatterns = [
    path("projects/", include("apps.projects.api.urls")),
]
