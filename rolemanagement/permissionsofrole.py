from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from core.models import Deposits , Receipts

# Use Group as the content type since these are role-level permissions
content_type, _ = ContentType.objects.get_or_create(
    app_label='auth',   # Groups are in the 'auth' app
    model='group'
)

role_permissions = [
    ("admin_dashboard_access", "Access Admin Dashboard"),
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



from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Receipts, Deposits   # ✅ adjust app/model names if needed

# --- Receipt Permissions ---
receipt_content_type, _ = ContentType.objects.get_or_create(
    app_label='core',     # replace with your app name
    model='receipts'       # lowercase model name
)

receipt_permissions = [
    ("list_receipts", "List Receipts"),
    ("download_receipts", "Download Receipts"),
 
]

created = 0
for codename, name in receipt_permissions:
    obj, created_flag = Permission.objects.get_or_create(
        codename=codename,
        name=name,
        content_type=receipt_content_type
    )
    if created_flag:
        print(f"[Created] {codename}")
        created += 1
    else:
        print(f"[Exists] {codename}")

# --- Deposit Permissions ---
deposit_content_type, _ = ContentType.objects.get_or_create(
    app_label='core',     # replace with your app name
    model='deposits'       # lowercase model name
)

deposit_permissions = [
   
    ("list_third_party_deposits", "List Third Party Deposits"),
    ("download_third_party_deposits", "Download Third Party Deposits"),
]

for codename, name in deposit_permissions:
    obj, created_flag = Permission.objects.get_or_create(
        codename=codename,
        name=name,
        content_type=deposit_content_type
    )
    if created_flag:
        print(f"[Created] {codename}")
        created += 1
    else:
        print(f"[Exists] {codename}")

print(f"\nDone. {created} new role permissions created.")
