from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Receipts
from core.receipt_email_service import (
    send_receipt_scheduled_reminder,
    should_send_scheduled_reminder,
)


class Command(BaseCommand):
    help = "Send receipt reminders on day 5 and then every 7 days until closure."

    def handle(self, *args, **options):
        today = timezone.localdate()
        total_sent = 0

        receipts = Receipts.objects.filter(status__iexact="Unused")

        for receipt in receipts:
            if not should_send_scheduled_reminder(receipt, today):
                continue

            if send_receipt_scheduled_reminder(receipt, today):
                total_sent += 1

        self.stdout.write(
            self.style.SUCCESS(f"Receipt reminder run completed. Emails sent: {total_sent}")
        )
