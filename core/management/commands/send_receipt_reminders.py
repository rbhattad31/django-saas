import logging
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Receipts
from core.receipt_email_service import (
    send_receipt_scheduled_reminder,
    should_send_scheduled_reminder,
)


class Command(BaseCommand):
    help = "Send receipt reminders on day 5 and then every 7 days until closure."

    def _get_daily_logger(self, today):
        core_dir = Path(__file__).resolve().parents[2]
        logs_dir = core_dir / "receipt_reminder_logs"
        logs_dir.mkdir(parents=True, exist_ok=True)

        log_file = logs_dir / f"{today.isoformat()}.log"

        logger = logging.getLogger("core.receipt_reminders")
        logger.setLevel(logging.INFO)
        logger.propagate = False

        if logger.handlers:
            logger.handlers.clear()

        handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger, log_file

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
        logger, log_file = self._get_daily_logger(today)

        receipt_number = options.get("receipt_number")
        logger.info("Receipt reminder run started. receipt_number=%s", receipt_number or "ALL")

        if receipt_number:
            receipts = Receipts.objects.filter(receipt_number=receipt_number, status__iexact="Unused")
            if not receipts.exists():
                logger.warning(
                    "Receipt number %s not found or not in Unused state.",
                    receipt_number,
                )
                self.stdout.write(
                    self.style.WARNING(f"Receipt number {receipt_number} not found or is not in Unused state.")
                )
                return
        else:
            receipts = Receipts.objects.filter(status__iexact="Unused")

        for receipt in receipts:
            if not should_send_scheduled_reminder(receipt, today):
                logger.info(
                    "Skipped receipt id=%s number=%s (schedule conditions not met).",
                    receipt.id,
                    receipt.receipt_number,
                )
                continue

            if send_receipt_scheduled_reminder(receipt, today):
                total_sent += 1
                logger.info(
                    "Sent reminder for receipt id=%s number=%s.",
                    receipt.id,
                    receipt.receipt_number,
                )
            else:
                logger.error(
                    "Failed to send reminder for receipt id=%s number=%s.",
                    receipt.id,
                    receipt.receipt_number,
                )

        logger.info("Receipt reminder run completed. Emails sent: %s", total_sent)

        self.stdout.write(
            self.style.SUCCESS(f"Receipt reminder run completed. Emails sent: {total_sent}")
        )
        self.stdout.write(f"Log file: {log_file}")
