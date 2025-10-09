from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Reset every user's password to their email address (hashed properly)."

    def handle(self, *args, **options):
        users = User.objects.all()
        total = users.count()
        updated = 0

        self.stdout.write(f"Found {total} users... updating passwords.")

        for user in users:
            if not user.email:
                self.stdout.write(f"Skipping user with no email: ID {user.id}")
                continue

            try:
                user.set_password(user.email)  # hash the email as password
                user.save(update_fields=['password'])
                updated += 1
            except Exception as e:
                self.stderr.write(f"Error updating {user.email}: {e}")

        self.stdout.write(self.style.SUCCESS(f"✅ Done. Updated {updated}/{total} users."))
