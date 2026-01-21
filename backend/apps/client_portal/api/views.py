from django.contrib.auth.hashers import check_password
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.client_portal.models import ClientUser, ProjectShareLink
from .serializers import ClientLoginSerializer

from django.http import FileResponse, Http404, HttpResponse
from apps.documents.models import Document


class ClientLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ClientLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            client_user = ClientUser.objects.get(email=email, is_active=True)
        except ClientUser.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not check_password(password, client_user.password_hash):
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        client_user.last_login_at = timezone.now()
        client_user.save(update_fields=["last_login_at"])

        return Response(
            {
                "access": f"CLIENT-{client_user.id}",
                "client": {
                    "id": client_user.id,
                    "name": client_user.name,
                    "email": client_user.email,
                    "language": client_user.language_preference,
                },
            }
        )

class ClientProjectByTokenAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            link = ProjectShareLink.objects.select_related("project").get(
                token_hash=token
            )
        except ProjectShareLink.DoesNotExist:
            return Response(
                {"error": "Invalid or expired link"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not link.is_valid():
            return Response(
                {"error": "Link expired"},
                status=status.HTTP_403_FORBIDDEN,
            )

        project = link.project

        data = {
            "project_number": project.project_number,
            "status": project.status,
            "milestones": [
                {
                    "id": m.id,
                    "name": m.name,
                    "status": m.status,
                }
                for m in project.milestones.all()
            ],
            "documents": [
                {
                    "id": d.id,
                    "file_name": d.file_name,
                    "download_url": f"/api/client/documents/{d.id}/download/",
                }
                for d in project.documents.filter(visible_to_client=True)
            ],
        }

        if link.can_view_financials:
            invoices = project.invoices.all()
            data["financials"] = {
                "total": sum(i.total for i in invoices),
                "balance": sum(i.balance for i in invoices),
            }

        link.last_used_at = timezone.now()
        link.save(update_fields=["last_used_at"])

        return Response(data)

class ClientDocumentDownloadAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, doc_id):
        token = request.GET.get("token")

        if not token:
            return Response(
                {"error": "Token required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            link = ProjectShareLink.objects.select_related("project").get(
                token_hash=token
            )
        except ProjectShareLink.DoesNotExist:
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not link.is_valid():
            return Response(
                {"error": "Token expired"},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            document = Document.objects.get(
                id=doc_id,
                project=link.project,
                visible_to_client=True,
            )
        except Document.DoesNotExist:
            raise Http404("Document not found")

        response = HttpResponse(
            document.file_blob,
            content_type=document.file_type,
        )
        response["Content-Disposition"] = (
            f'attachment; filename="{document.file_name}"'
        )
        response["Content-Length"] = document.file_size

        return response
