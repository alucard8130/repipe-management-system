from django.urls import path
from .views import ClientDocumentDownloadAPIView, ClientLoginAPIView, ClientProjectByTokenAPIView

urlpatterns = [
    path("auth/login/", ClientLoginAPIView.as_view(), name="client-login"),
    path("project/<str:token>/", ClientProjectByTokenAPIView.as_view(), name="client-project-token"),
    path("documents/<int:doc_id>/download/", ClientDocumentDownloadAPIView.as_view(), name="client-document-download"),
]
