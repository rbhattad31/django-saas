from datetime import timedelta

from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.utils import timezone
from django.conf import settings

from core.models import RentalDeals
import logging


logger = logging.getLogger("Rental_Deal")


class Command(BaseCommand):
    help = "Send reminder emails for rental draft deals based on age and reminder cadence."

    def handle(self, *args, **options):
        today = timezone.localdate()
        total_sent = 0

        drafts = RentalDeals.objects.filter(form_status='Incomplete', is_deleted='N',account_id=2)  # Adjust account_id as needed

        for deal in drafts:
            deal_date = self._get_deal_date(deal)
            if not deal_date:
                continue

            deal_age = (today - deal_date).days
            if deal_age < 15:
                continue

            # First email: if no reminder sent yet (last_reminder_date is null)
            if not deal.last_reminder_date:
                should_send = True
            else:
                # Subsequent emails: send only if 7+ days have passed since last reminder
                last_reminder_date = deal.last_reminder_date
                if hasattr(last_reminder_date, 'date'):
                    last_reminder_date = last_reminder_date.date()
                should_send = today >= (last_reminder_date + timedelta(days=7))

            if not should_send:
                continue

            recipient = self._get_broker_email(deal)
            if not recipient:
                continue
            print(f"Sending reminder for deal {deal.id} to {recipient} (Deal age: {deal_age} days, Last reminder: {deal.last_reminder_date})  should send: {should_send}")
            logger.info(f"Sending reminder for deal {deal.id} to {recipient} (Deal age: {deal_age} days, Last reminder: {deal.last_reminder_date})  should send: {should_send}")
            subject = self._build_subject(deal)
            body = self._build_body(deal, deal_age)

            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                to=[recipient],
            )
            email.send(fail_silently=False)

            deal.last_reminder_date = today
            deal.save(update_fields=['last_reminder_date'])

            total_sent += 1

        self.stdout.write(self.style.SUCCESS(f"Rental draft reminder run completed. Emails sent: {total_sent}"))

    def _get_deal_date(self, deal):
        for field_name in ['created_at']:
            value = getattr(deal, field_name, None)
            if value:
                if hasattr(value, 'date'):
                    return value.date()
                return value
        return None

    def _get_broker_email(self, deal):
        submitted_user = getattr(deal, 'submitted_by_user', None)
        
        if submitted_user and getattr(submitted_user, 'email', None):
            return submitted_user.email

        for field_name in ['agent_email', 'tenant_agent_email', 'owner_email', 'tenant_email']:
            value = getattr(deal, field_name, None)
            if value:
                return value

        return None

    def _build_subject(self, deal):
        ref = getattr(deal, 'reference_number', '') or getattr(deal, 'id', '')
        return f"Draft Rental Deal Reminder - {ref}"

    def _build_body(self, deal, deal_age):
        ref = getattr(deal, 'reference_number', '') or getattr(deal, 'id', '')
        return (
            f"Hello,\n\n"
            f"This is a reminder for an incomplete draft rental deal.\n\n"
            f"Reference: {ref}\n\n"
            f"Drafted on: {deal.created_at.date()}\n\n"
            f"It has been {deal_age} days since it was drafted.\n\n"
            f"Please complete the draft deal and submit it.\n\n"
            f"Thank you."
        )
