from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Adjust app_label/model to your actual Users model
content_type, _ = ContentType.objects.get_or_create(
    app_label="core",
    model="users"
)

custom_permissions = [
    ("reports_management", "Reports Management"),
    ("agent_commission_report", "Agent Commission Report"),
    ("agent_performance_report", "Agent Performance Report"),
]

created_count = 0
for codename, name in custom_permissions:
    _, created = Permission.objects.get_or_create(
        codename=codename,
        name=name,
        content_type=content_type,
    )
    if created:
        print(f"[Created] {codename}")
        created_count += 1
    else:
        print(f"[Exists] {codename}")

print(f"\nDone. {created_count} new permissions created.")