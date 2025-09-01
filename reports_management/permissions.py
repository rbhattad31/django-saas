from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Users  # Make sure this matches your model

# Adjust to your actual app label in apps.py
content_type, _ = ContentType.objects.get_or_create(
    app_label='core',
    model='users'
)

# Only keep the 3 new permissions
custom_permissions = [
    ("reports_management", "Reports Management"),
    ("agent_commission_report", "Agent Commission Report"),
    ("agent_performance_report", "Agent Performance Report"),
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
