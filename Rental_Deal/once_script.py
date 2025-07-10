from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from core.models import RentalDeals  # Replace with your actual app name

# Ensure content type exists for unmanaged model
content_type, _ = ContentType.objects.get_or_create(app_label='core', model='rentaldeals')

custom_permissions = [
    ("manage_rental_deals", "Rental Deals Management"),
    ("view_pending_rental_deals", "Pending Rental Deals"),
    ("view_approved_rental_deals", "Approved Rental Deals"),
    ("edit_approved_rental_deals", "Edit Approved Rental Deals"),
    ("enter_finance_rental_deals", "Entered finance Rental Deal"),

    ("edit_draft_rental_deals", "Edit Draft Rental Deal"),
    ("update_finance_status_rental_deals", "Update finance status Rental Deals"),
    ("generate_tenancy_contract_rental_deals", "Generate Tenancy Contract Rental Deal"),
    ("view_all_rental_deals", "All Rental Deals"),
    ("view_waiting_finance_rental_deals", "Waiting For Finance Rental Deals"),

    ("view_rejected_rental_deals", "Rejected Rental Deals"), 
    ("view_my_draft_rental_deals", "My Rental Deals Drafts"),
    ("view_admin_rental_fields", "Admin Rental Deal fields"),
    ("view_pending_finance_rental_deals", "Pending finance Rental Deals"),
    ("create_draft_rental_deals", "Create Draft Rental Deals"),

    ("comment_finance_rental_deals", "Finance comment Rental Deals"),
    ("update_amt_status_rental_deals", "Update Amt status Rental Deals"),
]

created = 0
for codename, name in custom_permissions: 
    obj, created_flag = Permission.objects.get_or_create(
        codename=codename,
        name=name,
        content_type=content_type
    )
    if created_flag:
        print(f"[Created] Created: {codename}")
        created += 1
    else:
        print(f"[exsisting]  Already exists: {codename}")

print(f"\nDone. {created} new permissions created.")