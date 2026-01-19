from decimal import Decimal
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.inventory.models import Material, InventoryMovement
from apps.projects.models import Project
from apps.operations.models import WorkOrder
from apps.services.inventory_service import InventoryService
from .serializers import MaterialSerializer, InventoryMovementSerializer

#listar materiales con su stock actual
class MaterialListAPIView(generics.ListAPIView):
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Material.objects.filter(company=user.company, is_active=True)
    
#Karedex movimientos 
class InventoryMovementListAPIView(generics.ListAPIView):
    serializer_class = InventoryMovementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return InventoryMovement.objects.filter(company=user.company).order_by("-created_at")

#consumir stock de un material especifico
class ConsumeMaterialAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        try:
            material = Material.objects.get(id=data["material_id"], company=user.company)
            project = Project.objects.get(id=data["project_id"], company=user.company)

            work_order = None
            if data.get("work_order_id"):
                work_order = WorkOrder.objects.get(
                    id=data["work_order_id"],
                    project=project,
                )

            movement = InventoryService.consume_material(
                material=material,
                quantity=Decimal(data["quantity"]),
                project=project,
                work_order=work_order,
                reference_id=data.get("reference_id", ""),
                notes=data.get("notes", ""),
            )

            serializer = InventoryMovementSerializer(movement)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    
