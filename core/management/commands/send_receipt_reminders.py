from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Receipts
from core.receipt_email_service import (
    send_receipt_scheduled_reminder,
    should_send_scheduled_reminder,
)


class Command(BaseCommand):
    help = "Send receipt reminders on day 5 and then every 7 days until closure."

    def add_arguments(self, parser):
        parser.add_argument(
            "--receipt-number",
            type=int,
            dest="receipt_number",
            default=None,
            help="If provided, process only the receipt with this receipt number.",
        )

    def handle(self, *args, **options):
        today = timezone.localdate()
        total_sent = 0

        receipt_number = options.get("receipt_number")
        if receipt_number:
            receipts = Receipts.objects.filter(receipt_number=receipt_number, status__iexact="Unused")
            if not receipts.exists():
                self.stdout.write(
                    self.style.WARNING(f"Receipt number {receipt_number} not found or is not in Unused state.")
                )
                return
        else:
            receipts = Receipts.objects.filter(status__iexact="Unused")

        for receipt in receipts:
            if not should_send_scheduled_reminder(receipt, today):
                continue

            if send_receipt_scheduled_reminder(receipt, today):
                total_sent += 1

        self.stdout.write(
            self.style.SUCCESS(f"Receipt reminder run completed. Emails sent: {total_sent}")
        )
