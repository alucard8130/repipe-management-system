from rest_framework import serializers
from apps.client_portal.models import ClientUser, ProjectShareLink


class ClientLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ClientUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUser
        fields = ["id", "email", "name", "language_preference"]


class ProjectShareLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectShareLink
        fields = ["token_hash", "expires_at"]
