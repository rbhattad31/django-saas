# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
 

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser, Group
from django.contrib.auth.models import Permission

from django_multitenant.models import TenantModel, TenantManager
from datetime import datetime, date
from django.db.models import F




class GroupProfile(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name="profile")
    account = models.ForeignKey("core.Account", on_delete=models.CASCADE , default  = 2)  # your account model
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.account_id} - {self.group.name}"

# from Rental_Deal.serializers import User
# from django_multitenant.models import TenantModel, TenantManager




# class AccountHasPermission(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     account = models.ForeignKey('Account', on_delete=models.DO_NOTHING, db_column='account_id')
#     role = models.ForeignKey('Role', on_delete=models.DO_NOTHING, db_column='role_id')
#     permission = models.ForeignKey('Permission', on_delete=models.DO_NOTHING, db_column='permission_id')

#     class Meta:
#         db_table = 'account_has_permissions'
#         managed = False

#     def __str__(self):
#         return f"{self.account_id}-{self.role_id}-{self.permission_id}"


class Account(models.Model):
    id = models.BigAutoField(primary_key=True)
    account_name = models.CharField(max_length=191, unique=True)
    account_domain = models.CharField(max_length=191, unique=True)
    contact_name = models.CharField(max_length=191, null=True, blank=True)
    contact_email = models.CharField(max_length=191, null=True, blank=True)
    contact_phone = models.CharField(max_length=191, null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)
    logo = models.TextField(null=True, blank=True)
    plan = models.CharField(max_length=191, null=True, blank=True)
    max_users = models.CharField(max_length=191, null=True, blank=True)
    min_users = models.CharField(max_length=191, null=True, blank=True)
    is_active = models.CharField(
        max_length=1, choices=[('Y', 'Yes'), ('N', 'No'), ('A', 'Active'), ('R', 'Rejected')],
        default='N'
    )
    is_deleted = models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')], default='N')
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=191, null=True, blank=True)
    updated_by = models.CharField(max_length=191, null=True, blank=True)
    is_approved = models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')], default='N')

    class Meta:
        db_table = 'accounts'
        managed = False

    def __str__(self):
        return self.account_name
   
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if the account is being created for the first time
        super().save(*args, **kwargs)  # Save the Accoun

    # Default Django permissions (CRUD)
       
        if is_new:
            roles = {
            "Admin": [

                # fot the rental Deal Management   Permisions for the Admin
                # ✅ Full access
                "add_rentaldeals",
                "change_rentaldeals",
                "delete_rentaldeals",
                "view_rentaldeals",
                "manage_rental_deals",
                "view_pending_rental_deals",
                "view_approved_rental_deals",
                "edit_approved_rental_deals",
                "enter_finance_rental_deals",
                "edit_draft_rental_deals",
                "update_finance_status_rental_deals",
                "generate_tenancy_contract_rental_deals",
                "view_all_rental_deals",
                "view_waiting_finance_rental_deals",
                "view_rejected_rental_deals",
                
                "view_my_draft_rental_deals",
                "view_admin_rental_fields",
                "view_pending_finance_rental_deals",
                "create_draft_rental_deals",
                "update_amt_status_rental_deals",
                "comment_finance_rental_deals",


                #Sale Deal Managment Permison for ad admin 
                "add_salesdeals",
                "change_salesdeals",
                "delete_salesdeals",
                "view_salesdeals",

                "manage_sales_deals",
                "view_all_sales_deals",
                "view_pending_sales_deals",
                "view_approved_sales_deals",
                "view_rejected_sales_deals",
                "view_waiting_finance_sales_deals",
                "add_salesdeals",
                "change_salesdeals",
                "view_salesdeals",
                "view_my_draft_sales_deals",# 
                "delete_salesdeals",
                "view_admin_sales_fields",
                "edit_approved_sales_deals",
                "view_pending_finance_sales_deal",#view_pending_finance_sales_deal
                "enter_finance_sales_deal", #
                "create_draft_sales_deal",
                "edit_draft_sales_deal",
                "update_aml_status_sales_deal",
                "update_finance_status_sales_deal",
                "comment_finance_sales_deal",

                # Property Management   for admin
                "property_management_rentalproperties",
                "add_rentalproperties",
                "property_rentalproperties",
                "draft_rentalproperties",  

                "create_draft_property_rentalproperties",
                "view_properties_rentalproperties",
                "edit_properties_rentalproperties",
                "delete_properties_rentalproperties",
                "edit_approved_properties_rentalproperties",
                "list_management_receipts_rentalproperties",
                "add_management_receipts_rentalproperties",
                "edit_management_receipts_rentalproperties",
                "view_management_receipts_rentalproperties",
                "download_management_receipts_rentalproperties",

                "pending_properties_rentalproperties",
                "approved_properties_rentalproperties",
                "rejected_properties_rentalproperties",
                "waiting_for_finance_properties_rentalproperties",
                "pending_finance_properties_rentalproperties",
                "entered_finance_properties_rentalproperties",

                "admin_properties_fields_rentalproperties",
                "update_aml_status_properties_rentalproperties",
                "update_finance_status_properties_rentalproperties",
                "finance_comment_properties_rentalproperties",

                












                # recipts Management permisiions for admin
                # rather than addong if user can see the Recipts Module a permission if user have any of receipts it will be visible
 	            "add_receipts",
 	            "change_receipts" ,
                "delete_receipts", # here i dont have download permission  but i am using delete permission  for that rather than creating   since just we need to check id permision presnet or not  so we can use delete for the download permission only 
                "view_receipts",
                "list_receipts",  
                "download_receipts",


                # Dashboard permissions for Admin.
                "total_users",
                "total_active_users",
                "total_inactive_users",

                "total_rental_deals",
                "rental_deal_drafts",
                "approved_rental_deals",
                "pending_rental_deals",
                "rejected_rental_deals",
                "waiting_finance_rental_deals",
                "total_gross_commission_rental",
                "total_net_commission_rental",
                "entered_finance_rental_deals",
                "pending_finance_rental_deals",

                "total_sale_deals",
                "sale_deal_drafts",
                "approved_sale_deals",
                "pending_sale_deals",
                "rejected_sale_deals",
                "waiting_finance_sales_deals",
                "total_gross_commission_sales",
                "total_net_commission_sales",
                "entered_finance_sales_deals",
                "pending_finance_sales_deals",

                "total_property",
                "property_drafts",
                "approved_properties",
                "pending_properties",
                "rejected_properties",
                "waiting_finance_properties",
                "pending_finance_properties",
                "entered_finance_properties",
                "total_gross_commission_properties",
                "total_net_commission_properties",

                "receipts_count",
                "third_party_receipts_count",
                "management_receipts_count",

                # thrid party receipts management for the admin
                "add_deposits",
                "change_deposits",
                "delete_deposits",
                "view_deposits",
                "list_third_party_deposits",
                "download_third_party_deposits",


                #   Role  management for admin
                "admin_dashboard_access",
                "add_group",
                "change_group",
                "view_group",
                "role_management",
                "user&role_management",

                #user permissions for Admin
                 
                 
                "update_profile_password",
                "user_management",
                "add_users",
                "change_users",
                "view_users",
                "accounts_management",


                # Report management permissions for admin
               
                'reports_management',
                "agent_commission_report",
                "agent_performance_report",




            ],
            "Manager": [
                # Real Deal MAnagement Permission for the Manager
                "manage_rental_deals",
                "view_pending_rental_deals",
                "view_approved_rental_deals",
                "view_rentaldeals",
                # "edit_approved_rental_deals",  # this is not manage approved for some having edit and somenot having edit 
                "view_all_rental_deals",
                "view_rejected_rental_deals",
                "change_rentaldeals",
                "view_my_draft_rental_deals",

                 #Sale Deal Managment Permison for mANAGE
                "manage_sales_deals",
                "view_all_sales_deals",
                "view_pending_sales_deals",
                "view_rejected_sales_deals",
                "change_salesdeals",
                "view_salesdeals",
                 "view_my_draft_sales_deals",


                #  Property  Management for the   Manager 
                "property_management_rentalproperties",
                "draft_rentalproperties",
                "view_properties_rentalproperties",
                
                "edit_properties_rentalproperties",
                "list_management_receipts_rentalproperties",
                "view_management_receipts_rentalproperties",
                "download_management_receipts_rentalproperties",

                "pending_properties_rentalproperties",
                "approved_properties_rentalproperties",
                "rejected_properties_rentalproperties",




                # recipts management for the Mananger 
                "view_receipts",
                "list_receipts",  
                 

                # dashBroad Permissions for the Manager
                "rental_deal_drafts",
                "approved_rental_deals",
                "pending_rental_deals",
                "rejected_rental_deals",
                "waiting_finance_rental_deals",
                "total_gross_commission_rental",
                "total_net_commission_rental",
                "sale_deal_drafts",
                "approved_sale_deals",
                "pending_sale_deals",
                "rejected_sale_deals",
                "waiting_finance_sales_deals",
                "total_gross_commission_sales",
                "total_net_commission_sales",
                 
                #therid party receipts management for the manager

                "view_deposits",
                "list_third_party_deposits",
                 

                # User & Role  management for admin
                "admin_dashboard_access",
                 
                #user permissions for Admin
                 




            ],
            "Agent": [
                # Real Deal MAnagement Permission for the Agent
                "manage_rental_deals",
                "view_pending_rental_deals",
                "view_approved_rental_deals",
                "add_rentaldeals",
                "view_rentaldeals",
                "edit_draft_rental_deals",
                "generate_tenancy_contract_rental_deals",
                "view_all_rental_deals",
                "view_rejected_rental_deals",
                "change_rentaldeals",
                "view_my_draft_rental_deals",
                "create_draft_rental_deals",

                 #Sale Deal Managment Permison for ad admin 
                "manage_sales_deals",
                "view_all_sales_deals",
                "view_pending_sales_deals",
                "view_approved_sales_deals",
                "add_salesdeals",
                "change_salesdeals",
                "view_salesdeals",
                "view_my_draft_sales_deals",
                "create_draft_sales_deal",
                "edit_draft_sales_deal",

                # Property Managment for the Agent  
                "property_management_rentalproperties",
                "property_rentalproperties",
                "draft_rentalproperties",
                "add_rentalproperties",
                "create_draft_property_rentalproperties",
                "view_properties_rentalproperties",
                "edit_properties_rentalproperties",

                "pending_properties_rentalproperties",
                "approved_properties_rentalproperties",
                "rejected_properties_rentalproperties",





                # recipts management for the Agent 


                # Dash Broad Persmissions for the Agent
                'total_rental_deals',
                "rental_deal_drafts",
                "approved_rental_deals",
                "pending_rental_deals",
                "rejected_rental_deals",
                "total_gross_commission_rental",
                "total_net_commission_rental",
                "sale_deal_drafts",
                "approved_sale_deals",
                "pending_sale_deals",
                "rejected_sale_deals",
                "total_gross_commission_sales",
                "total_net_commission_sales",
                "total_property",
                "property_drafts",
                "approved_properties",
                "pending_properties",
                "rejected_properties",

                # thrid party receipts management for the Agent


                # User & Role  management for admin
                "admin_dashboard_access",

                #user permissions for the Agent
                "update_profile_password",
                
                
            ],
            "Finance": [

                # Real Deal MAnagement Permission for the Finance
                "manage_rental_deals",
                "view_rentaldeals",
                "enter_finance_rental_deals",
                "update_finance_status_rental_deals",
                "view_pending_finance_rental_deals",
                "update_amt_status_rental_deals",
                "comment_finance_rental_deals",



                 #Sale Deal Managment Permison for Finac
                "manage_sales_deals",
                "view_salesdeals",
                "view_pending_finance_sales_deal",
                "enter_finance_sales_deal",
                "update_aml_status_sales_deal",
                "update_finance_status_sales_deal",
                "comment_finance_sales_deal",

                 # Property Managment for the  Finance 
                "property_management_rentalproperties",
                "add_rentalproperties",
                "view_properties_rentalproperties",
                "list_management_receipts_rentalproperties",
                "add_management_receipts_rentalproperties",
                "edit_management_receipts_rentalproperties",
                "view_management_receipts_rentalproperties",
                "download_management_receipts_rentalproperties",

                "waiting_for_finance_properties_rentalproperties",
                "pending_finance_properties_rentalproperties",
                "entered_finance_properties_rentalproperties",

                "update_aml_status_properties_rentalproperties",
                "update_finance_status_properties_rentalproperties",
                "finance_comment_properties_rentalproperties",






                 # recipts management for the Finace  
                # rather than addong if user can see the Recipts Module a permission if user have any of receipts it will be visible
 	            "add_receipts",
 	            "change_receipts", 
                "delete_receipts", # here i dont have download permission  but i am using delete permission  for that rather than creating   since just we need to check id permision presnet or not  so we can use delete for the download permission only 
                "view_receipts",
                "list_receipts",  
                "download_receipts",

                # dash broad Permisions
                "entered_finance_rental_deals",
                "pending_finance_rental_deals",
                "entered_finance_sales_deals",
                "pending_finance_sales_deals",
                "pending_finance_properties",
                "entered_finance_properties",


                # third party receipts management for the Finance
                "view_deposits",
                "add_deposits",
                "change_deposits",
                "delete_deposits",
                "list_third_party_deposits",
                "download_third_party_deposits",

                # User & Role  management for admin
                "admin_dashboard_access",
                #user permissions for the Agent
                "update_profile_password",
                


                ],
            }
            for role, permissions in roles.items():
                group_name = f"{self.id}-{role}"
                group, _ = Group.objects.get_or_create(name=group_name)

                for codename in permissions:
                    try:
                        perm = Permission.objects.get(codename=codename)
                        group.permissions.add(perm)
                    except Permission.DoesNotExist:
                        print(f"⚠️ Permission '{codename}' not found — please make sure it exists.")

                GroupProfile.objects.get_or_create(
                    group=group,
                    defaults={
                        "account": self,
                        "is_active": True  # or False if you want to deactivate by default
                    }
                )
        
            # Create default roles only after the Account is saved and has a valid ID
            # default_roles = ['Admin', 'Manager', 'Agent','Finance']
            # for role in default_roles:
            #     group_name = f"{self.id}-{role}"
            #     Group.objects.get_or_create(name=group_name)





# class TenantBaseModel(TenantModel):
#     # account = models.ForeignKey(Account, on_delete=models.CASCADE)

#     tenant_id = 'account'
#     objects = TenantManager() 

#     class Meta:
#         abstract = True



# class Branches(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     account = models.ForeignKey(Account, models.DO_NOTHING, blank=True, null=True)
#     branch_name = models.CharField(max_length=191)
#     branch_address = models.CharField(max_length=191)
#     is_deleted = models.CharField(max_length=1)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'branches'


# class Chronicles(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     account_id = models.IntegerField()
#     email_address_id = models.IntegerField()
#     email_content_id = models.IntegerField()
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'chronicles'


# class Cities(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     name = models.CharField(max_length=191)
#     status = models.CharField(max_length=8)
#     state = models.ForeignKey('States', models.DO_NOTHING)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     created_by = models.CharField(max_length=191)
#     updated_by = models.CharField(max_length=191, blank=True, null=True)
#     is_deleted = models.CharField(max_length=1)

#     class Meta:
#         managed = False
#         db_table = 'cities'


# class Configurations(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     no_of_days = models.CharField(max_length=191)
#     email_address = models.CharField(max_length=191)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     email_frequency = models.CharField(max_length=191)
#     reminder_email_team = models.CharField(max_length=191)
#     account_id = models.IntegerField()

#     class Meta:
#         managed = False
#         db_table = 'configurations'


# class Countries(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     code = models.CharField(max_length=191, blank=True, null=True)
#     name = models.CharField(max_length=191)
#     status = models.CharField(max_length=8)
#     phonecode = models.IntegerField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     created_by = models.CharField(max_length=191)
#     updated_by = models.CharField(max_length=191, blank=True, null=True)
#     is_deleted = models.CharField(max_length=1)

#     class Meta:
#         managed = False
#         db_table = 'countries'

 


# class DropdownTypes(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     dropdown_name = models.CharField(unique=True, max_length=191)
#     dependent_dropdown = models.CharField(max_length=191, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'dropdown_types'


# class Dropdowns(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     dropdown = models.ForeignKey(DropdownTypes, models.DO_NOTHING, blank=True, null=True)
#     dropdown_value = models.CharField(max_length=191)
#     status = models.CharField(max_length=8)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     created_by = models.CharField(max_length=191)
#     updated_by = models.CharField(max_length=191, blank=True, null=True)
#     is_deleted = models.CharField(max_length=1)

#     class Meta:
#         managed = False
#         db_table = 'dropdowns'


# class EmailAddresses(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     email_address = models.CharField(max_length=191)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     account_id = models.IntegerField()

#     class Meta:
#         managed = False
#         db_table = 'email_addresses'


# class EmailAddresss(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     email_address = models.CharField(max_length=191)
#     is_deleted = models.CharField(max_length=1)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     account_id = models.IntegerField()

#     class Meta:
#         managed = False
#         db_table = 'email_addresss'


# class EmailContents(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     email_subject = models.CharField(max_length=191)
#     email_body = models.CharField(max_length=191)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     is_deleted = models.CharField(max_length=1)
#     account_id = models.IntegerField()

#     class Meta:
#         managed = False
#         db_table = 'email_contents'


# class FailedJobs(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     connection = models.TextField()
#     queue = models.TextField()
#     payload = models.TextField()
#     exception = models.TextField()
#     failed_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'failed_jobs'


# class Features(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     name = models.CharField(max_length=191)

#     class Meta:
#         managed = False
#         db_table = 'features'


# class Images(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     property = models.ForeignKey('Properties', models.DO_NOTHING)
#     url = models.CharField(max_length=191)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'images'


# class ManagementReceipts(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     date = models.DateField()
#     receipt_number = models.BigIntegerField()
#     dhs = models.CharField(max_length=191)
#     fils = models.CharField(max_length=191)
#     cheque_no = models.CharField(max_length=191)
#     bank = models.CharField(max_length=191)
#     sec_date = models.DateField()
#     being = models.CharField(max_length=191)
#     status = models.CharField(max_length=191)
#     deal_type = models.CharField(max_length=191)
#     received_from = models.CharField(max_length=191, blank=True, null=True)
#     payment_type = models.CharField(max_length=191, blank=True, null=True)
#     deal_refer_no = models.CharField(max_length=191)
#     sum_of_dhs = models.CharField(max_length=191)
#     agent_name = models.CharField(max_length=191)
#     project_name = models.CharField(max_length=191)
#     building_name = models.CharField(max_length=191)
#     unit_number = models.CharField(max_length=191)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     account_id = models.IntegerField()

#     class Meta:
#         managed = False
#         db_table = 'management_receipts'


# class Migrations(models.Model):
#     migration = models.CharField(max_length=191)
#     batch = models.IntegerField()

#     class Meta:
#         managed = False
#         db_table = 'migrations'


# class ModelHasPermissions(models.Model):
#     permission = models.ForeignKey('Permission', on_delete=models.DO_NOTHING)
#     model_type = models.CharField(max_length=191)
#     model_id = models.PositiveBigIntegerField()

#     class Meta:
#         unique_together = ('permission', 'model_id', 'model_type')
#         db_table = 'model_has_permissions'
#         managed = False


# class ModelHasRoles(models.Model):
#     role = models.ForeignKey('Role', on_delete=models.DO_NOTHING)
#     model_type = models.CharField(max_length=191)
#     model_id = models.PositiveBigIntegerField()

#     class Meta:
#         managed = False  # Only if you're mapping an existing table
#         db_table = 'model_has_roles'
#         unique_together = ('role', 'model_type', 'model_id')


# class PasswordResets(models.Model):
#     email = models.CharField(max_length=191)
#     token = models.CharField(max_length=191)
#     created_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'password_resets'


# class Permission(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     name = models.CharField(max_length=191)
#     screen = models.CharField(max_length=191, null=True, blank=True)
#     is_deleted = models.CharField(max_length=191, default='N')
#     guard_name = models.CharField(max_length=191)
#     created_at = models.DateTimeField(null=True, blank=True)
#     updated_at = models.DateTimeField(null=True, blank=True)
#     account_id = models.CharField(max_length=191, null=True, blank=True)

#     class Meta:
#         db_table = 'permissions'
#         managed = False

#     def __str__(self):
#         return self.name


# class Plans(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     planname = models.CharField(max_length=191)
#     planprice = models.IntegerField()
#     minimumusers = models.IntegerField()
#     maximumusers = models.IntegerField()
#     status = models.CharField(max_length=8)
#     is_deleted = models.CharField(max_length=191, blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'plans'


class Properties(models.Model):
    id = models.BigAutoField(primary_key=True)
    bayut_property_ref_no = models.CharField(unique=True, max_length=191)
    property_status = models.CharField(max_length=7)
    permit_number = models.BigIntegerField()
    property_purpose = models.CharField(max_length=4)
    property_parent_type = models.CharField(max_length=11)
    property_type = models.CharField(max_length=16)
    furnished = models.CharField(max_length=3, blank=True, null=True)
    city = models.CharField(max_length=191)
    locality = models.CharField(max_length=191)
    sub_locality = models.CharField(max_length=191, blank=True, null=True)
    tower_name = models.CharField(max_length=191, blank=True, null=True)
    bayut_location_id = models.IntegerField()
    property_title = models.CharField(max_length=191, blank=True, null=True)
    property_description = models.TextField(blank=True, null=True)
    property_size = models.IntegerField()
    property_size_unit = models.CharField(max_length=191)
    bedrooms = models.IntegerField()
    bathroom = models.IntegerField()
    price = models.IntegerField()
    rent_frequency = models.CharField(max_length=191, blank=True, null=True)
    listing_agent = models.CharField(max_length=191, blank=True, null=True)
    listing_agent_phone = models.CharField(max_length=191, blank=True, null=True)
    listing_agent_email = models.CharField(max_length=191, blank=True, null=True)
    off_plan = models.CharField(max_length=191, blank=True, null=True)
    featured_on_company_website = models.CharField(max_length=5, blank=True, null=True)
    exclusive_rights = models.CharField(max_length=3, blank=True, null=True)
    geopoints_latitude = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True)
    geopoints_longitude = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True)
    completion_status = models.CharField(max_length=191, blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'properties'


# class PropertyFeatures(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     property = models.ForeignKey(Properties, models.DO_NOTHING)
#     feature = models.ForeignKey(Features, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'property_features'


class Receipts(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    receipt_number = models.BigIntegerField()
    dhs = models.CharField(max_length=191)
    fils = models.CharField(max_length=191)
    cheque_no = models.CharField(max_length=191,blank=True, null=True)
    bank = models.CharField(max_length=191,blank=True, null=True)
    sec_date = models.DateField()
    being = models.CharField(max_length=191)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=191)
    deal_type = models.CharField(max_length=191)
    received_from = models.CharField(max_length=191, blank=True, null=True)
    payment_type = models.CharField(max_length=191, blank=True, null=True)
    deal_refer_no = models.CharField(max_length=191,blank=True ,null =True)
    sum_of_dhs = models.CharField(max_length=191)
    agent_name = models.CharField(max_length=191)
    project_name = models.CharField(max_length=191)
    building_name = models.CharField(max_length=191)
    unit_number = models.CharField(max_length=191)
    account_id = models.IntegerField()
    agent_id = models.IntegerField()
    agent_email = models.CharField(max_length=255)
    mail_status = models.CharField(max_length=255 ,blank=True,null=True)

    class Meta:
        managed = False
        db_table = 'receipts'


class ReceiptReminderLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    receipt = models.ForeignKey(
        Receipts,
        on_delete=models.CASCADE,
        db_column='receipt_id',
        related_name='reminder_logs',
    )
    receipt_number = models.BigIntegerField()
    sent_to = models.CharField(max_length=255)
    agent_name = models.CharField(max_length=191, blank=True, null=True)
    reminder_type = models.CharField(max_length=20)   # 'created', 'day_1', 'day_5', 'recurring'
    day_number = models.IntegerField(blank=True, null=True)  # days since receipt creation
    sent_at = models.DateTimeField()
    status = models.CharField(max_length=10)          # 'success' or 'failed'
    error_message = models.TextField(blank=True, null=True)
    triggered_by = models.CharField(max_length=20, default='cron')  # 'cron' or 'manual'
    account_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'receipt_reminder_log'

    def __str__(self):
        return f"Receipt {self.receipt_number} | {self.reminder_type} | {self.status} | {self.sent_at}"








# class RoleHasPermission(models.Model):
#     permission = models.ForeignKey(Permission, on_delete=models.CASCADE, db_column='permission_id')
#     role = models.ForeignKey('Role', on_delete=models.CASCADE, db_column='role_id')

#     class Meta:
#         db_table = 'role_has_permissions'
#         managed = False
#         unique_together = (('permission', 'role'),)

#     def __str__(self):
#         return f"{self.role_id} - {self.permission_id}"

# class Role(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     name = models.CharField(max_length=191)
#     account = models.ForeignKey(Account, on_delete=models.DO_NOTHING, db_column='account_id')
#     description = models.CharField(max_length=191)
#     created_by = models.CharField(max_length=191)
#     updated_by = models.CharField(max_length=191, null=True, blank=True)
#     is_deleted = models.CharField(max_length=191, default='N')
#     guard_name = models.CharField(max_length=191)
#     created_at = models.DateTimeField(null=True, blank=True)
#     updated_at = models.DateTimeField(null=True, blank=True)
#     is_active = models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')], default='Y')

#     class Meta:
#         db_table = 'roles'
#         managed = False

#     def __str__(self):
#         return self.name


# 
#  
# class Settings(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     name = models.CharField(max_length=191)
#     value = models.TextField()
#     setting_type = models.CharField(max_length=191, blank=True, null=True)
#     account = models.ForeignKey(Account, models.DO_NOTHING)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     created_by = models.CharField(max_length=191)
#     updated_by = models.CharField(max_length=191, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'settings'


# class States(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     name = models.CharField(max_length=191)
#     country = models.ForeignKey(Countries, models.DO_NOTHING)
#     status = models.CharField(max_length=8)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     created_by = models.CharField(max_length=191)
#     updated_by = models.CharField(max_length=191, blank=True, null=True)
#     is_deleted = models.CharField(max_length=1)

#     class Meta:
#         managed = False
#         db_table = 'states'


# class Timezones(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     country = models.CharField(max_length=191)
#     timezone = models.CharField(max_length=191)
#     gmt_offset = models.CharField(max_length=191)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'timezones'


# class UserAccounts(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey('Users', models.DO_NOTHING)
#     account = models.ForeignKey(Account, models.DO_NOTHING, blank=True, null=True)
#     is_deleted = models.CharField(max_length=1)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     created_by = models.CharField(max_length=191)
#     updated_by = models.CharField(max_length=191, blank=True, null=True)

    # class Meta:
    #     managed = False
    #     db_table = 'user_accounts'


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password :
            user.set_password(password)
         
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # extra_fields.setdefault('role', Role.objects.get(id=1))

        if not extra_fields.get('name'):
            extra_fields['name'] = 'Admin'
             
        
        
        return self.create_user(email, password, **extra_fields)


class Users(AbstractUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=191, blank=True, null=True)
    username = None 
    mobile_number = models.CharField(max_length=191)
    # role = models.ForeignKey('Role', on_delete=models.DO_NOTHING, db_column='role', related_name='users' ,null = True,blank=True)
    email = models.CharField(unique=True, max_length=191)
    password = models.CharField(max_length=191)
    gender = models.CharField(max_length=6, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    timezone = models.CharField(max_length=191, blank=True, null=True)
    is_active = models.BooleanField(default=1)
    is_deleted = models.CharField(max_length=1)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    last_login  = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=191,blank=True)
    updated_by = models.CharField(max_length=191, blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    # OR 'user_account_id' if you use db_column
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # or 'users_set'
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # or 'users_permissions'
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

   


    objects = CustomUserManager()
    # tenant_objects = TenantManager()

    
     


    # djagno searche sfor Lastlogin but ue are using diff filed so make it present but not in DB
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    

    class Meta:
        # managed = False
        db_table = 'users'


# class Videos(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     property = models.ForeignKey(Properties, models.DO_NOTHING)
#     url = models.CharField(max_length=191)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'videos'

# Renal Deal Management 
class RentalDealQuerySet(models.QuerySet):
    def with_user(self):
        # Optimized join: RentalDeal → submitted_by_user
        return self.annotate(
            user_id=F("submitted_by_user__id"),
            user_name=F("submitted_by_user__name"),   # 👈 using your custom "name"
            user_email=F("submitted_by_user__email"),
            user_mobile=F("submitted_by_user__mobile_number"),
            
        )

class RentalDeals (models.Model):
    submitted_date = models.DateField(blank=True, null=True)
    submitted_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    reference_number = models.CharField(max_length=191, unique=True)
    date = models.DateField()
    unit_details = models.TextField()
    building_name = models.TextField()
    project_name = models.TextField()
    is_new_deal = models.CharField(max_length=1, choices=[('R', 'R'),   ('N', 'N')], default='N')
    owner_title = models.TextField(blank=True, null=True)
    owner_first_name = models.TextField()
    owner_last_name = models.TextField(blank=True, null=True)
    owner_source = models.TextField()
    owner_mobile = models.TextField()
    owner_email = models.TextField(blank=True, null=True)
    tenant_title = models.TextField(blank= True ,null=True , default='N/A')
    tenant_first_name = models.TextField()
    tenant_last_name = models.TextField(blank=True, null=True)
    tenant_source = models.TextField()
    tenant_mobile = models.TextField()
    tenant_email = models.TextField(blank=True, null=True)
    owner_agency = models.TextField()
    agent_first_name = models.TextField()
    agent_last_name = models.TextField(blank=True, null=True)
    agent_phone = models.TextField()
    agent_email = models.TextField(blank=True, null=True)
    brn = models.TextField(blank=True, null=True)
    tenant_agency = models.TextField()
    tenant_agent_first_name = models.TextField()
    tenant_agent_last_name = models.TextField(blank=True, null=True)
    tenant_agent_phone = models.TextField()
    tenant_agent_email = models.TextField(blank=True, null=True)
    tenant_brn = models.TextField(blank=True, null=True)
    tenancy_contract = models.TextField()
    owner_passport_copy = models.TextField()
    tenant_passport_visa_copy = models.TextField()
    tenant_emirates_id = models.TextField(blank=True, null=True)
    rental_deposit_cheque_copy = models.TextField()
    title_deed = models.TextField()
    owner_poa_pp_copy = models.TextField(blank=True, null=True)
    key_hand_over_form = models.TextField(blank=True, null=True)
    total_commission = models.TextField()
    less_outsude_commission = models.TextField()
    net_commission = models.TextField()
    classic = models.TextField()
    agent1 = models.TextField()
    agent2 = models.TextField(blank=True, null=True)
    agent3 = models.TextField(blank=True, null=True)
    is_approved_rejected = models.CharField(
    max_length=1,
    choices=[
        ('P', 'Pending'),
        ('F', 'Waiting Finance'),
        ('A', 'Approved'),
        ('R', 'Rejected')
    ],
    default='P'
)  
    approved_rejected_by = models.TextField(blank=True, null=True)
    is_entered_in_finance_system = models.CharField(max_length=1, choices=[('0', 'No'), ('1', 'Yes')], default='0')
    comments = models.TextField(blank=True, null=True)
    rental_price = models.TextField(blank=True, null=True)
    ejari = models.TextField(blank=True, null=True)
    agent_name1 = models.TextField(blank=True, null=True)
    agent_name2 = models.TextField(blank=True, null=True)
    agent_name3 = models.TextField(blank=True, null=True)
    owner_eid_copy = models.TextField(blank=True, null=True)
    agent_comment = models.TextField(blank=True, null=True)
    mediating_agency = models.TextField(blank=True, null=True)
    mediating_agent_name = models.TextField(blank=True, null=True)
    mediating_agent_phone = models.TextField(blank=True, null=True)
    mediating_agent_email = models.TextField(blank=True, null=True)
    mediating_agency_brn = models.TextField(blank=True, null=True)
    poa_copy = models.TextField(blank=True, null=True)
    deal_start_date = models.DateField()
    deal_end_date = models.DateField()
    receipt_no = models.TextField()
    receipt_no2 = models.TextField(blank=True, null=True)
    receipt_no3 = models.TextField(blank=True, null=True)
    receipt_no4 = models.TextField(blank=True, null=True)
    receipt_no5 = models.TextField(blank=True, null=True)
    form_status = models.CharField(max_length=10, choices=[('Complete', 'Complete'), ('Incomplete', 'Incomplete')], blank=True, null=True)
    rental_kyc_number = models.TextField()
    is_rental_aml = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], blank=True, null=True)
    kyc_number = models.TextField(blank=True, null=True)
    comments_finance = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=191, blank=True, null=True)
    updated_by = models.CharField(max_length=191, blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING, null=True, blank=True ,db_column='account_id')
    property = models.ForeignKey('properties', on_delete=models.SET_NULL, blank=True, null=True)
    #branch = models.ForeignKey('branches', on_delete=models.SET_NULL, blank=True, null=True)
    is_deleted = models.CharField(max_length=1, choices=[('Y', 'Y'), ('N', 'N')], default='N')
    plot_no = models.TextField(blank=True, null=True)
    mode_of_payment = models.TextField(blank=True, null=True)
    deal_agent = models.CharField(max_length=191, blank=True, null=True)
    receipt_id = models.IntegerField(default=0)
    receipt_id2 = models.IntegerField(default=0)
    receipt_id3 = models.IntegerField(default=0)
    receipt_id4 = models.IntegerField(default=0)
    receipt_id5 = models.IntegerField(default=0)
    property_usage = models.CharField(max_length=191,blank=True ,null =True)
    property_size = models.CharField(max_length=191,blank=True ,null =True)
    premises_no = models.CharField(max_length=191, blank= True ,null = True )
    security_deposit = models.CharField(max_length=191, blank=True ,null =True )
    submitted_by_agent = models.IntegerField()
    property_type = models.CharField(max_length=191, blank=True, null=True)
    tenancy_application_form = models.TextField(blank=True, null=True)
    screening = models.TextField()
    commission_shortfall_form_copy = models.TextField(blank=True, null=True)
    screening_comments = models.TextField(blank=True)
    seller_nationality = models.CharField(max_length=191)
    buyer_nationality = models.CharField(max_length=191)
    manager_approved_rejected = models.CharField(max_length=1, choices=[('P', 'Pending'), ('A', 'Approved'),('R', 'Rejected')], default='P')
    re_submitted_date = models.DateField( blank=True, null=True)
    last_reminder_date = models.DateField(blank=True, null=True)
    receipts_list = models.TextField(blank=True, null=True)  # Store receipt IDs as a comma-separated string


    # tenant_id = 'account'  # OR 'user_account_id' if you use db_column

    # objects = TenantManager()

    objects = RentalDealQuerySet.as_manager()

    
    class Meta:
        managed = False
        db_table = 'rental_deals'
        indexes = [
            # ✅ Solo indexes
            models.Index(fields=["form_status"], name="idx_form_status"),
            models.Index(fields=["is_deleted"], name="idx_is_deleted"),
            models.Index(fields=["is_approved_rejected"], name="idx_is_approved_rejected"),
            models.Index(fields=["manager_approved_rejected"], name="idx_manager_approved_rejected"),
            models.Index(fields=["is_entered_in_finance_system"], name="idx_finance_entered"),

            # ✅ Composite indexes
            models.Index(fields=["is_deleted", "account"], name="idx_deleted_account"),
            models.Index(fields=["form_status", "account"], name="idx_formstatus_account"),
            models.Index(fields=["is_approved_rejected", "form_status"], name="idx_rejected_complete"),
            models.Index(fields=["manager_approved_rejected", "form_status"], name="idx_mgr_rejected_complete"),
            models.Index(fields=["is_entered_in_finance_system", "form_status"], name="idx_finance_complete"),
            models.Index(fields=["form_status", "created_by"], name="idx_draft_admin"),
            models.Index(fields=["form_status", "submitted_by_user"], name="idx_draft_agent"),
        ]


class SaleDealQuerySet(models.QuerySet):
    def with_user(self):
        # Optimized join: RentalDeal → submitted_by_user
        return self.annotate(
            user_id=F("submitted_by_user__id"),
            user_name=F("submitted_by_user__name"),   # 👈 using your custom "name"
            user_email=F("submitted_by_user__email"),
            user_mobile=F("submitted_by_user__mobile_number"),
            
        )

# sale deal management  

class SalesDeals(models.Model):
    id = models.AutoField(primary_key=True) 
    submitted_date = models.DateField(blank=True, null=True )
    re_submitted_date = models.DateField( blank=True, null=True)
    submitted_by_user = models.ForeignKey(Users, models.DO_NOTHING)
    date = models.DateField()
    reference_number = models.TextField()
    unit_details = models.TextField()
    builduing_name = models.TextField()
    project_name = models.TextField()
    developer_details = models.TextField(blank=True, null=True)
    seller_name = models.TextField()
    seller_source = models.TextField()
    selller_mobile = models.TextField()
    seller_email = models.TextField(blank=True, null=True)
    buyer_name = models.TextField()
    buyer_source = models.TextField()
    buyer_mobile = models.TextField()
    buyer_email = models.TextField(blank=True, null=True)
    seller_agency = models.TextField(blank=True, null=True)
    seller_agent_name = models.TextField(blank=True, null=True )
    seller_agent_phone = models.TextField(blank=True, null=True)
    seller_agent_email = models.TextField(blank=True, null=True)
    seller_agency_brn = models.TextField(blank=True, null=True)
    buyer_agency = models.TextField(blank=True, null=True)
    buyer_agent_name = models.TextField(blank=True, null=True)
    buyer_agent_phone = models.TextField(blank=True, null=True)
    buyer_agent_email = models.TextField(blank=True, null=True)
    buyer_agency_brn = models.TextField(blank=True, null=True)
    mediating_agency = models.TextField(blank=True, null=True)
    mediating_agent_name = models.TextField(blank=True, null=True)
    mediating_agent_phone = models.TextField(blank=True, null=True)
    mediating_agent_email = models.TextField(blank=True, null=True)
    mediating_agency_brn = models.TextField(blank=True, null=True)
    signed_mou = models.TextField(blank=True, null=True)
    new_title_deed = models.TextField(blank=True, null=True)
    old_title_deed = models.TextField(blank=True, null=True)
    owners_passport_copy = models.TextField(blank=True, null=True)
    buyers_passport_copy = models.TextField(blank=True, null=True)
    buyers_deposit_cheque_copy = models.TextField(blank=True, null=True)
    sellers_deposit_cheque_copy = models.TextField(blank=True, null=True)
    seller_poa_passport_copy = models.TextField(blank=True, null=True)
    buyer_poa_passport_copy = models.TextField(blank=True, null=True)
    total_commission = models.TextField(blank=True, null=True)
    less_outsude_commission = models.TextField(blank=True, null=True)
    net_commission = models.TextField(blank=True, null=True)
    classic = models.TextField(blank=True, null=True)
    agent1 = models.TextField(blank=True, null=True)
    agent2 = models.TextField(blank=True, null=True)
    agent3 = models.TextField(blank=True, null=True)
    is_approved_rejected = models.CharField(
    max_length=1,
    choices=[
        ('P', 'Pending'),
        ('F', 'Waiting Finance'),
        ('A', 'Approved'),
        ('R', 'Rejected')
    ],
    default='P'
) 
    approved_rejected_by = models.TextField(blank=True, null=True)
    is_entered_in_finance_system = models.CharField(max_length=1,choices=[('0', 'No'), ('1', 'Yes')], default='0')
    comments = models.TextField(blank=True, null=True)
    deal_amount = models.TextField(blank=True, null=True)
    owner_eid_copy = models.TextField(blank=True, null=True)
    agent_name1 = models.TextField(blank=True, null=True)
    agent_name2 = models.TextField(blank=True, null=True)
    agent_name3 = models.TextField(blank=True, null=True)
    buyer_eid = models.TextField(blank=True, null=True)
    agent_comment = models.TextField(blank=True, null=True)
    receipt_no = models.TextField(blank=True, null=True)
    receipt_no2 = models.TextField(blank=True, null=True)
    receipt_no3 = models.TextField(blank=True, null=True)
    receipt_no4 = models.TextField(blank=True, null=True)
    receipt_no5 = models.TextField(blank=True, null=True)
    seller_poa_copy = models.TextField(blank=True, null=True)
    buyer_poa_copy = models.TextField(blank=True, null=True)
    buyer_poa_eid = models.TextField(blank=True, null=True)
    seller_poa_eid = models.TextField(blank=True, null=True)
    form_status = models.CharField(max_length=10, choices=[('Complete', 'Complete'), ('Incomplete', 'Incomplete')], blank=True, null=True)
    sale_kyc_number = models.TextField(blank=True, null=True)
    form_i_copy = models.TextField(blank=True, null=True)
    referral_agreement_copy = models.TextField(blank=True, null=True)
    management_approval_form_copy = models.TextField(blank=True, null=True)
    commission_shortfall_form_copy = models.TextField(blank=True, null=True)
    is_sale_aml = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], blank=True, null=True)
    kyc_number = models.TextField(blank=True, null=True)
    comments_finance = models.TextField(blank=True, null=True)
    type_of_purchase = models.CharField(max_length=100, blank=True , null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=191)
    updated_by = models.CharField(max_length=191, blank=True, null=True)
    account = models.ForeignKey(Account, models.DO_NOTHING, blank=True, null=True,default=True)
    property = models.ForeignKey(Properties, models.DO_NOTHING, blank=True, null=True)
    # branch = models.ForeignKey(Branches, models.DO_NOTHING, blank=True, null=True)
    is_deleted = models.CharField(max_length=1,default="N", choices=[('Y', 'Y'), ('N', 'N')])
    deal_agent = models.CharField(max_length=191, blank=True, null=True)
    receipt_id = models.CharField(max_length=191 , default=0)
    receipt_id2 = models.CharField(max_length=191 , default=0)
    receipt_id3 = models.CharField(max_length=191 , default=0)
    receipt_id4 = models.CharField(max_length=191 , default=0)
    receipt_id5 = models.CharField(max_length=191 , default=0)
    submitted_by_agent = models.IntegerField()
    screening = models.TextField()
    screening_comments = models.TextField()
    seller_nationality = models.CharField(max_length=191)
    buyer_nationality = models.CharField(max_length=191)
    manager_cheque_copy = models.TextField(blank=True, null=True)
    manager_approved_rejected = models.CharField(max_length=1, choices=[('P', 'Pending'), ('A', 'Approved'),('R', 'Rejected')], default='P')


    objects = SaleDealQuerySet.as_manager()

    class Meta:
        managed = False
        db_table = 'sales_deals'


#  Thrid party recipcepts 
class Deposits(models.Model):
    date = models.DateField()
    deposit_number = models.BigIntegerField()
    dhs = models.CharField(max_length=191)
    fils = models.CharField(max_length=191)
    cheque_no = models.CharField(max_length=191 ,blank= True , null  = True)
    bank = models.CharField(max_length=191 , blank= True  , null=True)
    sec_date = models.DateField()
    being = models.CharField(max_length=191)
    status = models.CharField(max_length=191 ,blank=True, null=True)
    deal_type = models.CharField(max_length=191)
    received_from = models.CharField(max_length=191, null=True, blank=True)
    payment_type = models.CharField(max_length=191, null=True, blank=True)
    deal_refer_no = models.CharField(max_length=191 ,null = True , blank = True  )
    sum_of_dhs = models.CharField(max_length=191)
    agent_name = models.CharField(max_length=191, null =True ,blank=True)
    project_name = models.CharField(max_length=191)
    building_name = models.CharField(max_length=191)
    unit_number = models.CharField(max_length=191)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    account_id = models.IntegerField()
    on_behalf_of = models.CharField(max_length=191)

    def __str__(self):
        return f"Deposit #{self.deposit_number} - {self.cheque_no}"
    
    class Meta:
        managed = False
        db_table = 'deposits'









 

#  Property Management  Models 

class RentalProperties(models.Model):
    id = models.BigAutoField(primary_key=True)
    #deal_date = models.TextField()
    deal_date = models.CharField(max_length=10, blank=True, null=True)  # Stores dd-mm-yyyy
    reference_number = models.TextField()
    #pms = models.TextField(blank= True , null = True)
    
    project_name = models.TextField()
    building_name = models.TextField()
    unit_details = models.TextField()
    pms_price = models.TextField()
    # pm_start_date = models.TextField()
    # pm_end_date = models.TextField()
    # tenancy_start_date = models.TextField()
    # tenancy_end_date = models.TextField()
    pm_start_date = models.CharField(max_length=10, blank=True, null=True)
    pm_end_date = models.CharField(max_length=10, blank=True, null=True)
    tenancy_start_date = models.CharField(max_length=10, blank=True, null=True)
    tenancy_end_date = models.CharField(max_length=10, blank=True, null=True)
    owner_first_name = models.TextField()
    owner_source = models.TextField()
    owner_mobile = models.TextField()
    owner_email = models.TextField()
    agency_name = models.TextField()
    agent_name = models.TextField()
    brn = models.TextField(blank=True, null=True)
    agent_phone = models.TextField()
    agent_email = models.TextField(blank=True, null=True)
    no_of_cheque = models.TextField()
    cheque_date = models.TextField()

    #cheque_date = models.JSONField(blank=True, null=True)
    #cheque_date = models.DateField(null=True, blank=True)
    
    pms_contract = models.TextField()
    owner_passport_copy = models.TextField()
    owner_eid_copy = models.TextField(blank=True ,null=True)
    pms_cheque_copy = models.TextField()
    title_deed = models.TextField()
    poa_pp = models.TextField(blank=True, null=True)
    poa_copy = models.TextField(blank=True, null=True)
    key_hand_over_form = models.TextField(blank=True, null=True)
    # pms_contract = models.FileField(upload_to='uploads/', null=True, blank=True)
    # owner_passport_copy = models.FileField(upload_to='uploads/', null=True, blank=True)
    # owner_eid_copy = models.FileField(upload_to='uploads/', null=True, blank=True)
    # pms_cheque_copy = models.FileField(upload_to='uploads/', null=True, blank=True)
    # title_deed = models.FileField(upload_to='uploads/', null=True, blank=True)
    # poa_pp = models.FileField(upload_to='uploads/', null=True, blank=True)
    # poa_copy = models.FileField(upload_to='uploads/', null=True, blank=True)
    # key_hand_over_form = models.FileField(upload_to='uploads/', null=True, blank=True)
    # kyc_form = models.FileField(upload_to='uploads/', null=True, blank=True)
    kyc_form = models.TextField(blank=True, null=True)
    kyc_number = models.TextField(blank=True, null=True)
    total_commission = models.TextField()
    less_outside_commission = models.TextField()
    net_commission = models.TextField()
    classic = models.TextField()
    agent1 = models.TextField()
    agent2 = models.TextField(blank=True, null=True)
    agent3 = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    agent_name1 = models.TextField(blank=True, null=True)
    agent_name2 = models.TextField(blank=True, null=True)
    agent_name3 = models.TextField(blank=True, null=True)
    receipt_no = models.TextField()
    receipt_no2 = models.TextField(blank=True, null=True)
    receipt_no3 = models.TextField(blank=True, null=True)
    receipt_no4 = models.TextField(blank=True, null=True)
    receipt_no5 = models.TextField(blank=True, null=True)
    form_status = models.CharField(
        max_length=50,
        choices=[
            ('Complete', 'Complete'),
            ('Incomplete', 'Incomplete')
        ],
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=191, blank=True, null=True)
    updated_by = models.CharField(max_length=191, blank=True, null=True)
    #account = models.ForeignKey(Accounts, models.DO_NOTHING, blank=True, null=True)
    account = models.ForeignKey(Account, models.DO_NOTHING, blank=True, null=True,db_column='account_id')

      

    status = models.CharField(max_length=20, choices = [
        ('Active', 'Active'),
        ('About To Expire', 'About To Expire'),
        ('Expired', 'Expired'),
        ('Renew', 'Renew'),
        ('Closed', 'Closed'),
        ('Inactive', 'Inactive'),
    ], default='Active')
    # deal_sno = models.IntegerField()
    deal_sno = models.IntegerField(null=True,blank=True)
    #is_approved_rejected = models.CharField(max_length=1)
    # is_approved_rejected = models.CharField(max_length=1, null=False, blank=True)
    is_approved_rejected = models.CharField(max_length=1,choices=[('P','pending'),("A","Approved"),('R',"Rejected"),('W',"Waiting Finance")] ,  null=True, blank=True,default="P")

    approved_rejected_by = models.TextField(blank=True, null=True)
    is_entered_in_finance_system = models.CharField(max_length=1)
    comments_finance = models.TextField(blank=True, null=True)
    submitted_by_user_id = models.IntegerField()
    is_deleted = models.CharField(max_length=1,choices=[('Y','Y'),('N','N')],default='N')
    agent_comment = models.TextField(blank=True, null=True)
    is_property_aml = models.CharField(max_length=3)
    screening = models.TextField()
    commission_shortfall_form_copy = models.TextField(blank=True, null=True)
    screening_comments = models.TextField( blank=True ,null=True)
    seller_nationality = models.CharField(max_length=191)
    buyer_nationality = models.CharField(max_length=191 ,blank=True ,null=True)
    submitted_date = models.DateField()
    re_submitted_date = models.DateField(blank=True, null=True)
    
    # manager_approved_rejected = models.CharField(
    #     max_length=1,
    #     choices=[
            
    #         ('A', 'Approved'),
    #         ('R', 'Rejected'),
    #     ],
    #     null=True,
    #     blank=True,
        
    # )
    manager_approved_rejected = models.CharField(
        max_length=1,
        choices=[
            ('P', 'Pending'),
            ('A', 'Approved'),
            ('R', 'Rejected'),
        ],
        default='P',  # Default stored value, not in choices
        null=True,
        blank=True,
    )

    class Meta:
        managed = False
        db_table = 'rental_properties'

    def debug_form_status(self):
        print(f"\nForm Status: {self.form_status} (Length: {len(self.form_status) if self.form_status else 0})")


    
    def update_status_if_needed(self):
        #print(f"📌 Starting update_status_if_needed for property ID: {self.id}")

        # 👇 Add these two lines here
        #print(f"DEBUG - Account: {self.account}, Account ID: {self.account_id}")
        #print(f"DEBUG - Deal SNO: {self.deal_sno}")
        #print(f"Starting update_status_if_needed for property ID: {self.id}")

        # 1. Handle Incomplete form as Inactive status
        if self.form_status and self.form_status.strip() == 'Incomplete':
            if self.status != 'Inactive':
                print(f"Setting status to Inactive because form_status is Incomplete for property ID: {self.id}")
                self.status = 'Inactive'
                self.save(update_fields=['status'])
            # else:
            #     print(f"Status already Inactive for Incomplete form on property ID: {self.id}")
            return

        # 2. If no tenancy_end_date, do nothing
        if not self.tenancy_start_date:
            print(f"No tenancy_start_date for property ID: {self.id}")
            return

        #tenancy_end_date = self.tenancy_end_date.strip()
        tenancy_start_date = self.tenancy_start_date.strip()
        date_formats = ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%B %d, %Y"]
        tenancy_start = None

        for fmt in date_formats:
            try:
                tenancy_start = datetime.strptime(tenancy_start_date, fmt).date()
                #print(f"Parsed date with format {fmt}: {tenancy_start}")
                break
            except ValueError:
                continue

        if not tenancy_start:
            print(f"Failed to parse tenancy_start_date '{tenancy_start_date}' for property ID: {self.id}")
            return

        today = date.today()
        #print(f"Today: {today}, Tenancy start: {tenancy_start}")

        diff_days = (date.today() - tenancy_start).days

        
        if diff_days > 365:
            status = 'Expired'
        elif 320 < diff_days <= 365:
            status = 'About To Expire'
        else:
            status = 'Active'

        #print(f"🏷 Current status: {self.status}, New status: {status}")
        if self.status != status:
            #print(f"Updating status from {self.status} to {status} for property ID: {self.id}")
            try:
                self.status = status
                self.save(update_fields=['status'])
                #print(f"Status updated successfully for property ID: {self.id}")
            except Exception as e:
                print(f"Save error for property ID: {self.id}: {str(e)}")
        # else:
        #     print(f"Status already up to date: {status} for property ID: {self.id}")






class ManagementReceipts(models.Model):
    id = models.BigAutoField(primary_key=True)  # 1. Primary Key, Auto Increment, NOT NULL
    date = models.DateField(null=False)  # 2. NOT NULL
    receipt_number = models.CharField(max_length=100, null=True, blank=True)  # 3. NOT NULL
    dhs = models.CharField(max_length=191, null=False)  # 4. NOT NULL
    fils = models.CharField(max_length=191, null=False)  # 5. NOT NULL
    cheque_no = models.CharField(max_length=15, blank=True, null=True)  # 6. NOT NULL
    # bank = models.CharField(max_length=191, null=False)  # 7. NOT NULL
    bank = models.CharField(max_length=255, blank=True, null=True)
    sec_date = models.DateField(null=False)  # 8. NOT NULL
    being = models.CharField(max_length=191, null=False)  # 9. NOT NULL
    status = models.CharField(max_length=191, null=False)  # 10. NOT NULL
    # deal_type = models.CharField(max_length=191, null=False)  # 11. NOT NULL
    deal_type = models.CharField(max_length=50, choices=[
        ('Management Fee', 'Management Fee'),
        ('Ejari Fee', 'Ejari Fee')
    ])
    received_from = models.CharField(max_length=191, blank=True, null=True)  # 12. DEFAULT NULL
    # payment_type = models.CharField(max_length=191, blank=True, null=True)  # 13. DEFAULT NULL
    payment_type = models.CharField(max_length=50, choices=[
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque'),
        ('Bank Transfer', 'Bank Transfer')
    ])
    deal_refer_no = models.CharField(max_length=191, null=True,blank=True)  # 14. NOT NULL
    sum_of_dhs = models.CharField(max_length=191, null=False)  # 15. NOT NULL
    agent_name = models.CharField(max_length=191, null=False)  # 16. NOT NULL
    project_name = models.CharField(max_length=191, null=False)  # 17. NOT NULL
    building_name = models.CharField(max_length=191, null=False)  # 18. NOT NULL
    unit_number = models.CharField(max_length=191, null=False)  # 19. NOT NULL
    created_at = models.DateTimeField(blank=True, null=True)  # 20. DEFAULT NULL
    updated_at = models.DateTimeField(blank=True, null=True)  # 21. DEFAULT NULL
    # account_id = models.IntegerField(null=False)  # 22. NOT NULL
    account_id = models.IntegerField(null=True)  # 22. NOT NULL


    class Meta:
        #managed = False  # Assuming this model is managed outside of Django (existing DB table)
        db_table = 'management_receipts'

class Dashboard(models.Model):
    class Meta:
        managed = False  # Prevents table creation
    
  

        