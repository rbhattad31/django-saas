import json
import logging
from threading import Thread

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone

from core.models import Receipts, ReceiptReminderLog

logger = logging.getLogger("Rental_Deal")


def _parse_mail_status(raw_status):
    if not raw_status:
        return {}

    if isinstance(raw_status, dict):
        return raw_status

    try:
        parsed = json.loads(raw_status)
        if isinstance(parsed, dict):
            return parsed
    except (TypeError, ValueError):
        pass

    # Legacy value fallback, for values like "sent".
    return {"legacy": str(raw_status)}


def _safe_dump_status(data):
    payload = json.dumps(data, separators=(",", ":"))
    # DB column size is 255. Truncate safely if needed.
    if len(payload) > 255:
        data = {
            "created": data.get("created"),
            "last": data.get("last"),
            "count": data.get("count", 0),
        }
        payload = json.dumps(data, separators=(",", ":"))
    return payload


def _save_status(receipt, status_dict):
    receipt.mail_status = _safe_dump_status(status_dict)
    receipt.save(update_fields=["mail_status"])


def _get_created_date(receipt):
    created = receipt.created_at or receipt.updated_at
    if created is not None:
        if hasattr(created, "date"):
            return created.date()
        return created
    return receipt.date


def _build_receipt_subject(receipt, prefix="Receipt Reminder"):
    return f"{prefix} - Receipt {receipt.receipt_number}"


def _build_receipt_body(receipt, message_line):
    return (
        f"Hello,\n\n"
        f"{message_line}\n\n"
        f"Receipt Number: {receipt.receipt_number}\n"
        f"Deal Reference: {receipt.deal_refer_no or '-'}\n"
        f"Amount (DHS): {receipt.dhs}\n"
        f"Unit: {receipt.unit_number}\n"
        f"Project: {receipt.project_name}\n"
        f"Status: {receipt.status}\n\n"
        f"Please complete the related closure process.\n\n"
        f"Thank you."
    )


def _send_email(receipt, subject, body):
    recipient = (receipt.agent_email or "").strip()
    if not recipient:
        logger.warning("Receipt %s skipped: missing agent_email", receipt.id)
        return False

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
        to=[recipient],
    )
    email.send(fail_silently=False)
    return True


def send_receipt_created_email(receipt_id):
    receipt = Receipts.objects.filter(id=receipt_id).first()
    if not receipt:
        return

    status_data = _parse_mail_status(receipt.mail_status)
    if status_data.get("created") == "sent":
        return

    subject = _build_receipt_subject(receipt, prefix="Receipt Created")
    body = _build_receipt_body(receipt, "A new receipt has been created.")

    try:
        sent = _send_email(receipt, subject, body)
    except Exception:
        logger.exception("Receipt created email failed for receipt %s", receipt.id)
        return

    if sent:
        status_data["created"] = "sent"
        status_data["created_at"] = timezone.localdate().isoformat()
        status_data.setdefault("count", 0)
        _save_status(receipt, status_data)

    ReceiptReminderLog.objects.create(
        receipt=receipt,
        receipt_number=receipt.receipt_number,
        sent_to=(receipt.agent_email or "").strip(),
        agent_name=receipt.agent_name,
        reminder_type="created",
        day_number=0,
        sent_at=timezone.now(),
        status="success" if sent else "failed",
        triggered_by="cron",
        account_id=receipt.account_id,
    )


def send_receipt_created_email_async(receipt_id):
    # Thread-based background dispatch so API call returns immediately.
    worker = Thread(target=send_receipt_created_email, args=(receipt_id,), daemon=True)
    worker.start()


def should_send_scheduled_reminder(receipt, today):
    if (receipt.status or "").strip().lower() != "unused":
        return False

    status_data = _parse_mail_status(receipt.mail_status)
    if not (
        receipt.mail_status == "sent"
        or status_data.get("legacy") == "sent"
        or status_data.get("created") == "sent"
    ):
        print(f"Receipt {receipt.id} skipped: created email not sent yet.")
        return False

    created_date = _get_created_date(receipt)
    print(f"Receipt {receipt.id} created date: {created_date}, today: {today}")
    if not created_date:
        return False

    days_since = (today - created_date).days
    print(days_since)

    # Schedule: day 1, day 4, then every 7 days (day 11, 18, 25 ...). not include the created day as day 0, start count from the next day.
    is_day_1 = days_since == 1
    is_day_4_or_recurring = days_since >= 4 and (days_since - 4) % 7 == 0
    if not (is_day_1 or is_day_4_or_recurring):
        print("entered the schedule check - not a reminder day")
        return False

    last_sent = status_data.get("last")
    print("the last sent day", last_sent)
    if last_sent == today.isoformat() :
        print( " the last sent chekc condtion "  )
        return False

    return True


def send_receipt_scheduled_reminder(receipt, today):
    subject = _build_receipt_subject(receipt)
    body = _build_receipt_body(
        receipt,
        "This is a scheduled reminder. Reminders are sent on day 1, day 2, day 5, and every 7 days thereafter until closure is completed.",
    )

    sent = _send_email(receipt, subject, body)
    print(f"Receipt {receipt.id} scheduled reminder sent: {sent}")

    created_date = _get_created_date(receipt)
    days_since = (today - created_date).days if created_date else None

    if days_since == 1:
        reminder_type = "day_1"
    elif days_since == 4:
        reminder_type = "day_4"
    else:
        reminder_type = "recurring"

    ReceiptReminderLog.objects.create(
        receipt=receipt,
        receipt_number=receipt.receipt_number,
        sent_to=(receipt.agent_email or "").strip(),
        agent_name=receipt.agent_name,
        reminder_type=reminder_type,
        day_number=days_since,
        sent_at=timezone.now(),
        status="success" if sent else "failed",
        triggered_by="cron",
        account_id=receipt.account_id,
    )

    if not sent:
        return False

    status_data = _parse_mail_status(receipt.mail_status)
    status_data["last"] = today.isoformat()
    status_data["count"] = int(status_data.get("count", 0)) + 1
    _save_status(receipt, status_data)
    return True
