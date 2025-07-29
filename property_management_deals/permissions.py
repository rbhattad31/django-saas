from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from core.models import RentalProperties  # Make sure model is correctly imported

# Adjust to your actual app label in apps.py
content_type, _ = ContentType.objects.get_or_create(
    app_label='core',
    model='rentalproperties'
)

custom_permissions = [
    ("property_management_rentalproperties", "Property Management - Rental Properties"),
    ("property_rentalproperties", "Property - Rental Properties"),
    ("draft_rentalproperties", "Draft - Rental Properties"),
    ("create_property_rentalproperties", "Create Property - Rental Properties"),
    ("create_draft_property_rentalproperties", "Create Draft Property - Rental Properties"),
    ("view_properties_rentalproperties", "View Properties - Rental Properties"),
    ("edit_properties_rentalproperties", "Edit Properties - Rental Properties"),
    ("list_management_receipts_rentalproperties", "List Management Receipts - Rental Properties"),
    ("add_management_receipts_rentalproperties", "Add Management Receipts - Rental Properties"),
    ("edit_management_receipts_rentalproperties", "Edit Management Receipts - Rental Properties"),
    ("view_management_receipts_rentalproperties", "View Management Receipts - Rental Properties"),
    ("download_management_receipts_rentalproperties", "Download Management Receipts - Rental Properties"),
    ("pending_properties_rentalproperties", "Pending Properties - Rental Properties"),
    ("approved_properties_rentalproperties", "Approved Properties - Rental Properties"),
    ("rejected_properties_rentalproperties", "Rejected Properties - Rental Properties"),
    ("waiting_for_finance_properties_rentalproperties", "Waiting For Finance Properties - Rental Properties"),
    ("pending_finance_properties_rentalproperties", "Pending Finance Properties - Rental Properties"),
    ("entered_finance_properties_rentalproperties", "Entered Finance Properties - Rental Properties"),
    ("admin_properties_fields_rentalproperties", "Admin Properties Fields - Rental Properties"),
    ("update_aml_status_properties_rentalproperties", "Update AML Status - Rental Properties"),
    ("update_finance_status_properties_rentalproperties", "Update Finance Status - Rental Properties"),
    ("finance_comment_properties_rentalproperties", "Finance Comment - Rental Properties"),
    ("delete_properties_rentalproperties", "Delete Properties - Rental Properties"),
    ("edit_approved_properties_rentalproperties", "Edit Approved Properties - Rental Properties"),
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
        print(f"[Exists] Already exists: {codename}")

print(f"\nDone. {created} new permissions created.")
