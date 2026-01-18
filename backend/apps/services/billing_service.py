from decimal import Decimal
from django.utils import timezone
from django.db import models

from apps.billing.models import Invoice, Payment


class BillingService:
    """
    Lógica de negocio de facturación.
    """

    @staticmethod
    def calculate_invoice_balance(invoice: Invoice) -> Decimal:
        """
        Recalcula el saldo de la factura basado en pagos.
        """
        total_paid = (
            invoice.payments.aggregate(total=models.Sum("amount"))["total"]
            or Decimal("0.00")
        )

        balance = invoice.total - total_paid
        return balance

    @staticmethod
    def update_invoice_status(invoice: Invoice) -> None:
        """
        Actualiza el estatus de la factura según saldo y fechas.
        """
        today = timezone.now().date()

        if invoice.balance <= Decimal("0.00"):
            invoice.status = Invoice.STATUS_PAID
            invoice.balance = Decimal("0.00")

        elif invoice.balance < invoice.total:
            invoice.status = Invoice.STATUS_PARTIAL

        else:
            if invoice.due_date and invoice.due_date < today:
                invoice.status = Invoice.STATUS_OVERDUE
            else:
                invoice.status = Invoice.STATUS_SENT

        invoice.save(update_fields=["status", "balance", "updated_at"])

    @staticmethod
    def apply_payment(invoice: Invoice, payment: Payment) -> Invoice:
        """
        Aplica un pago a una factura y recalcula saldo y estatus.
        """
        # Seguridad básica
        if payment.amount <= 0:
            raise ValueError("Payment amount must be greater than zero")

        # Recalcular saldo
        invoice.balance = BillingService.calculate_invoice_balance(invoice)

        # Actualizar estatus
        BillingService.update_invoice_status(invoice)

        return invoice
