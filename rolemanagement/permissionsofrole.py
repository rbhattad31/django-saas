from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

# Use Group as the content type since these are role-level permissions
content_type, _ = ContentType.objects.get_or_create(
    app_label='auth',   # Groups are in the 'auth' app
    model='group'
)

role_permissions = [
    ("admin_dashboard_access", "Access Admin Dashboard"),
    ("role_add", "Add Roles"),
    ("role_view", "View Roles"),
    ("role_edit", "Edit Roles"),
    ("role_management" , "Role Management"),
    ("user&role_management" , "User & Role Management"),
    
    
]

created = 0
for codename, name in role_permissions:
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

print(f"\nDone. {created} new role permissions created.")