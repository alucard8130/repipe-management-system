from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.operations.models import WorkOrder
from apps.projects.models import ProjectMilestone


@receiver(post_save, sender=WorkOrder)
def workorder_status_change(sender, instance: WorkOrder, **kwargs):
    """
    Si se completa una WorkOrder, avanza el milestone relacionado.
    """
    if instance.status != WorkOrder.STATUS_COMPLETED:
        return

    milestones = ProjectMilestone.objects.filter(
        project=instance.project,
        status=ProjectMilestone.STATUS_PENDING,
    ).order_by("order")

    milestone = milestones.first()
    if milestone:
        milestone.status = ProjectMilestone.STATUS_DONE
        milestone.completed_at = instance.completed_at
        milestone.save(update_fields=["status", "completed_at"])
