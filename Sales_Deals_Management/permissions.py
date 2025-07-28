from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from core.models import SalesDeals  # Replace with the actual path to your model

# Define the content type for the model
content_type, _ = ContentType.objects.get_or_create(
    app_label='core',  # Replace 'core' with your actual app label
    model='salesdeals'  # Must be lowercase model name
)

# List of custom permissions to create
custom_permissions = [
    ("manage_sales_deals", "Sales Deals Management"),
    ("view_all_sales_deals", "All Sales Deals"),
    ("view_pending_sales_deals", "Pending Sales Deals"),
    ("view_approved_sales_deals", "Approved Sales Deals"),
    ("view_rejected_sales_deals", "Rejected Sales Deals"),
    ("view_waiting_finance_sales_deals", "Waiting For Finance Sales Deals"),
    ("view_my_draft_sales_deals", "My Sales Deals Drafts"),
    ("view_admin_sales_fields", "Admin Sales Deal fields"),
    ("edit_approved_sales_deals", "Edit Approved Sales Deals"),
    ("view_pending_finance_sales_deal", "Pending finance Sales Deal"),
    ("enter_finance_sales_deal", "Entered finance Sales Deal"),
    ("create_draft_sales_deal", "Create Draft Sales Deal"),
    ("edit_draft_sales_deal", "Edit Draft Sales Deal"),
    ("update_aml_status_sales_deal", "Update Aml status Sales Deal"),
    ("update_finance_status_sales_deal", "Update finance status Sales Deal"),
    ("comment_finance_sales_deal", "Finance comment Sales Deal"),
]

# Create or update each permission
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

print(f"Done. {created} new permissions created.")
