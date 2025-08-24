
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Users  # Replace with any valid model from your app

# Use any valid model from your app for content_type
content_type, _ = ContentType.objects.get_or_create(
    app_label="core",
    model="users"  # must be lowercase model name
)

custom_permissions = [
    ("update_profile_password", "Update Profile & Password"),
    ("user_management", "User Management"),
    ("accounts_management", "Accounts Management Main Menu"),
]

created = 0
for codename, name in custom_permissions:
    obj, created_flag = Permission.objects.get_or_create(
        codename=codename,
        name=name,
        content_type=content_type
    )
    if created_flag:
        print(f"[Created] {codename}")
        created += 1
    else:
        print(f"[Exists] {codename}")

print(f"\nDone. {created} new permissions created.")