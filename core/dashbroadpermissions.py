from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Dashboard  # Replace with a valid model from your app

# Use any valid model from your app for content_type
content_type, _ = ContentType.objects.get_or_create(
    app_label='core',
    model='dashboard'
)

# List of custom permissions
custom_permissions = [
    ("total_users", "Total Users"),
    ("total_active_users", "Total Active Users"),
    ("total_inactive_users", "Total InActive Users"),

    ("total_rental_deals", "Total Rental Deals Count"),
    ("rental_deal_drafts", "Rental Deal Drafts Count"),
    ("approved_rental_deals", "Approved Rental Deals Count"),
    ("pending_rental_deals", "Pending Rental Deals Count"),
    ("rejected_rental_deals", "Rejected Rental Deals Count"),
    ("waiting_finance_rental_deals", "Waiting For Finance Rental Deals Count"),
    ("total_gross_commission_rental", "Total Gross commission Rental Deals Count"),
    ("total_net_commission_rental", "Total Net commission Rental Deals Count"),
    ("entered_finance_rental_deals", "Entered finance Rental Deals Count"),
    ("pending_finance_rental_deals", "Pending finance Rental Deals Count"),

    ("total_sale_deals", "Total Sale Deals Count"),
    ("sale_deal_drafts", "Sale Deal Drafts Count"),
    ("approved_sale_deals", "Approved Sale Deals Count"),
    ("pending_sale_deals", "Pending Sale Deals Count"),
    ("rejected_sale_deals", "Rejected Sales Deals Count"),
    ("waiting_finance_sales_deals", "Waiting For Finance Sales Deals Count"),
    ("total_gross_commission_sales", "Total Gross commission Sales Deals Count"),
    ("total_net_commission_sales", "Total Net commission Sales Deals Count"),
    ("entered_finance_sales_deals", "Entered finance Sales Deals Count"),
    ("pending_finance_sales_deals", "Pending finance Sales Deals Count"),

    ("total_property", "Total Property Count"),
    ("property_drafts", "Property Drafts Count"),
    ("approved_properties", "Approved Properties Count"),
    ("pending_properties", "Pending Properties Count"),
    ("rejected_properties", "Rejected Properties Count"),
    ("waiting_finance_properties", "Waiting For Finance Properties Count"),
    ("pending_finance_properties", "Pending finance Properties Count"),
    ("entered_finance_properties", "Entered finance Properties Count"),
    ("total_gross_commission_properties", "Total Gross commission Properties Count"),
    ("total_net_commission_properties", "Total Net commission Properties Count"),

    ("receipts_count", "Receipts Count"),
    ("third_party_receipts_count", "Third Party Receipts Count"),
    ("management_receipts_count", "Management Receipts Count"),
]

created = 0
for codename, name in custom_permissions:
    obj, created_flag = Permission.objects.get_or_create(
        codename=codename,
        name=name,
        content_type=content_type
    )
    if created_flag:
        print("[Created] Created: " + codename)
        created += 1
    else:
        print("[Exists] Already exists: " + codename)

print("\nDone. {} new permissions created.".format(created))
