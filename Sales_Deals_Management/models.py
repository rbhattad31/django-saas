from django.db import models
from core.models import Users
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group,  Permission



# class Accounts(models.Model):
#     id = models.AutoField(primary_key=True)
#     account_name = models.CharField(unique=True, max_length=191)
#     account_domain = models.CharField(unique=True, max_length=191)
#     contact_name = models.CharField(max_length=191, blank=True, null=True)
#     contact_email = models.CharField(max_length=191, blank=True, null=True)
#     contact_phone = models.CharField(max_length=191, blank=True, null=True)
#     additional_info = models.TextField(blank=True, null=True)
#     logo = models.TextField(blank=True, null=True)
#     plan = models.CharField(max_length=191, blank=True, null=True)
#     max_users = models.CharField(max_length=191, blank=True, null=True)
#     min_users = models.CharField(max_length=191, blank=True, null=True)
#     is_active = models.CharField(max_length=1)
#     is_deleted = models.CharField(max_length=1)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     created_by = models.CharField(max_length=191, blank=True, null=True)
#     updated_by = models.CharField(max_length=191, blank=True, null=True)
#     is_approved = models.CharField(max_length=1)

#     class Meta:
#         managed = False
#         db_table = 'accounts'
    

#     def __str__(self):
#         return self.account_name

#     def save(self, *args, **kwargs):
#         is_new = self.pk is None
#         super().save(*args, **kwargs)

#         if is_new:
#             roles = {
#                 "Admin": [
#                     # ✅ Full Sales Deals Access
#                     "add_salesdeals",
#                     "change_salesdeals",
#                     "delete_salesdeals",
#                     "view_salesdeals",

#                     "manage_sales_deals",
#                     "view_all_sales_deals",
#                     "view_pending_sales_deals",
#                     "view_approved_sales_deals",
#                     "view_rejected_sales_deals",
#                     "view_waiting_finance_sales_deals",
#                     "add_salesdeals",
#                     "change_salesdeals",
#                     "view_salesdeals",
#                     "my_sales_deals_drafts",
#                     "delete_salesdeals",
#                     "view_admin_sales_fields",
#                     "edit_approved_sales_deals",
#                     "view_pending_finance_sales_deals",
#                     "enter_finance_sales_deals",
#                     "create_draft_sales_deal",
#                     "edit_draft_sales_deal",
#                     "update_aml_status_sales_deal",
#                     "update_finance_status_sales_deal",
#                     "comment_finance_sales_deal",
#                 ],
#                 "Manager": [
#                     "manage_sales_deals",
#                     "view_all_sales_deals",
#                     "view_pending_sales_deals",
#                     "view_rejected_sales_deals",
#                     "change_salesdeals",
#                     "view_salesdeals",
#                     "view_my_draft_sales_deals",
#                 ],
#                 "Agent": [
#                     "manage_sales_deals",
#                     "view_all_sales_deals",
#                     "view_pending_sales_deals",
#                     "view_approved_sales_deals",
#                     "add_salesdeals",
#                     "change_salesdeals",
#                     "view_salesdeals",
#                     "view_my_draft_sales_deals",
#                     "create_draft_sales_deal",
#                     "edit_draft_sales_deal",
#                 ],
#                 "Finance": [
#                     "manage_sales_deals",
#                     "view_salesdeals",
#                     "view_pending_finance_sales_deal",
#                     "enter_finance_sales_deal",
#                     "update_aml_status_sales_deal",
#                     "update_finance_status_sales_deal",
#                     "comment_finance_sales_deal",
#                 ],
#             }

#             for role, permissions in roles.items():
#                 group_name = f"{self.id}-{role}"
#                 group, _ = Group.objects.get_or_create(name=group_name)

#                 for codename in permissions:
#                     try:
#                         perm = Permission.objects.get(codename=codename)
#                         group.permissions.add(perm)
#                     except Permission.DoesNotExist:
#                         print(f"⚠️ Permission '{codename}' not found — please ensure it's created.")



# class Branches(models.Model):
#     id = models.AutoField(primary_key=True)
#     account = models.ForeignKey(Accounts, models.DO_NOTHING, blank=True, null=True)
#     branch_name = models.CharField(max_length=191)
#     branch_address = models.CharField(max_length=191)
#     is_deleted = models.CharField(max_length=1)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'branches'


# class Properties(models.Model):
#     id = models.AutoField(primary_key=True)
#     bayut_property_ref_no = models.CharField(unique=True, max_length=191)
#     property_status = models.CharField(max_length=7)
#     permit_number = models.BigIntegerField()
#     property_purpose = models.CharField(max_length=4)
#     property_parent_type = models.CharField(max_length=11)
#     property_type = models.CharField(max_length=16)
#     furnished = models.CharField(max_length=3, blank=True, null=True)
#     city = models.CharField(max_length=191)
#     locality = models.CharField(max_length=191)
#     sub_locality = models.CharField(max_length=191, blank=True, null=True)
#     tower_name = models.CharField(max_length=191, blank=True, null=True)
#     bayut_location_id = models.IntegerField()
#     property_title = models.CharField(max_length=191, blank=True, null=True)
#     property_description = models.TextField(blank=True, null=True)
#     property_size = models.IntegerField()
#     property_size_unit = models.CharField(max_length=191)
#     bedrooms = models.IntegerField()
#     bathroom = models.IntegerField()
#     price = models.IntegerField()
#     rent_frequency = models.CharField(max_length=191, blank=True, null=True)
#     listing_agent = models.CharField(max_length=191, blank=True, null=True)
#     listing_agent_phone = models.CharField(max_length=191, blank=True, null=True)
#     listing_agent_email = models.CharField(max_length=191, blank=True, null=True)
#     off_plan = models.CharField(max_length=191, blank=True, null=True)
#     featured_on_company_website = models.CharField(max_length=5, blank=True, null=True)
#     exclusive_rights = models.CharField(max_length=3, blank=True, null=True)
#     geopoints_latitude = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True)
#     geopoints_longitude = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True)
#     completion_status = models.CharField(max_length=191, blank=True, null=True)
#     last_updated = models.DateTimeField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'properties'


# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field must be set")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#         return self.create_user(email, password, **extra_fields)

# class Users(AbstractBaseUser, PermissionsMixin):
#     id = models.BigAutoField(primary_key=True)
#     name = models.CharField(max_length=191)
#     mobile_number = models.CharField(max_length=191)
#     # role = models.IntegerField()
#     email = models.CharField(unique=True, max_length=191)
#     password = models.CharField(max_length=191)
#     gender = models.CharField(max_length=6, blank=True, null=True)
#     dob = models.DateField(blank=True, null=True)
#     additional_info = models.TextField(blank=True, null=True)
#     timezone = models.CharField(max_length=191, blank=True, null=True)
#     # is_active = models.CharField(max_length=1)
#     is_deleted = models.CharField(max_length=1)
#     remember_token = models.CharField(max_length=100, blank=True, null=True)
#     last_login = models.DateTimeField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     created_by = models.CharField(max_length=191)
#     updated_by = models.CharField(max_length=191, blank=True, null=True)
#     image = models.TextField(blank=True, null=True)
#     user_account_id = models.CharField(max_length=191)
#     is_active = models.BooleanField(default=True)  # Change from CharField
#     is_staff = models.BooleanField(default=False)  # Add this
#     is_superuser = models.BooleanField(default=False)


#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.email


#     class Meta:
#         # managed = False
#         db_table = 'users'


# class SalesDeals(models.Model):
#     id = models.AutoField(primary_key=True)
#     submitted_date = models.DateField()
#     submitted_by_user = models.ForeignKey(Users, models.DO_NOTHING)
#     date = models.DateField()
#     reference_number = models.TextField()
#     unit_details = models.TextField()
#     builduing_name = models.TextField()
#     project_name = models.TextField()
#     developer_details = models.TextField(blank=True, null=True)
#     seller_name = models.TextField()
#     seller_source = models.TextField()
#     selller_mobile = models.TextField()
#     seller_email = models.TextField(blank=True, null=True)
#     buyer_name = models.TextField()
#     buyer_source = models.TextField()
#     buyer_mobile = models.TextField()
#     buyer_email = models.TextField(blank=True, null=True)
#     seller_agency = models.TextField()
#     seller_agent_name = models.TextField()
#     seller_agent_phone = models.TextField()
#     seller_agent_email = models.TextField(blank=True, null=True)
#     seller_agency_brn = models.TextField(blank=True, null=True)
#     buyer_agency = models.TextField()
#     buyer_agent_name = models.TextField()
#     buyer_agent_phone = models.TextField()
#     buyer_agent_email = models.TextField(blank=True, null=True)
#     buyer_agency_brn = models.TextField(blank=True, null=True)
#     mediating_agency = models.TextField(blank=True, null=True)
#     mediating_agent_name = models.TextField(blank=True, null=True)
#     mediating_agent_phone = models.TextField(blank=True, null=True)
#     mediating_agent_email = models.TextField(blank=True, null=True)
#     mediating_agency_brn = models.TextField(blank=True, null=True)
#     signed_mou = models.TextField(blank=True, null=True)
#     new_title_deed = models.TextField(blank=True, null=True)
#     old_title_deed = models.TextField(blank=True, null=True)
#     owners_passport_copy = models.TextField(blank=True, null=True)
#     buyers_passport_copy = models.TextField(blank=True, null=True)
#     buyers_deposit_cheque_copy = models.TextField(blank=True, null=True)
#     sellers_deposit_cheque_copy = models.TextField(blank=True, null=True)
#     seller_poa_passport_copy = models.TextField(blank=True, null=True)
#     buyer_poa_passport_copy = models.TextField(blank=True, null=True)
#     total_commission = models.TextField()
#     less_outsude_commission = models.TextField()
#     net_commission = models.TextField()
#     classic = models.TextField()
#     agent1 = models.TextField()
#     agent2 = models.TextField(blank=True, null=True)
#     agent3 = models.TextField(blank=True, null=True)
#     is_approved_rejected = models.CharField(max_length=1)
#     approved_rejected_by = models.TextField(blank=True, null=True)
#     is_entered_in_finance_system = models.CharField(max_length=1)
#     comments = models.TextField(blank=True, null=True)
#     deal_amount = models.TextField(blank=True, null=True)
#     owner_eid_copy = models.TextField(blank=True, null=True)
#     agent_name1 = models.TextField(blank=True, null=True)
#     agent_name2 = models.TextField(blank=True, null=True)
#     agent_name3 = models.TextField(blank=True, null=True)
#     buyer_eid = models.TextField(blank=True, null=True)
#     agent_comment = models.TextField(blank=True, null=True)
#     receipt_no = models.TextField()
#     seller_poa_copy = models.TextField(blank=True, null=True)
#     buyer_poa_copy = models.TextField(blank=True, null=True)
#     buyer_poa_eid = models.TextField(blank=True, null=True)
#     seller_poa_eid = models.TextField(blank=True, null=True)
#     form_status = models.CharField(max_length=10, blank=True, null=True)
#     sale_kyc_number = models.TextField(blank=True, null=True)
#     is_sale_aml = models.CharField(max_length=3, blank=True, null=True)
#     kyc_number = models.TextField(blank=True, null=True)
#     comments_finance = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     created_by = models.CharField(max_length=191)
#     updated_by = models.CharField(max_length=191, blank=True, null=True)
#     account = models.ForeignKey(Accounts, models.DO_NOTHING, blank=True, null=True,default=True)
#     property = models.ForeignKey(Properties, models.DO_NOTHING, blank=True, null=True)
#     branch = models.ForeignKey(Branches, models.DO_NOTHING, blank=True, null=True)
#     is_deleted = models.CharField(max_length=1)
#     deal_agent = models.CharField(max_length=191, blank=True, null=True)
#     receipt_id = models.CharField(max_length=191)
#     submitted_by_agent = models.IntegerField()
#     screening = models.CharField(max_length=191)
#     screening_comments = models.TextField()
#     seller_nationality = models.CharField(max_length=191)
#     buyer_nationality = models.CharField(max_length=191)
#     manager_cheque_copy = models.TextField()
#     manager_approved_rejected = models.CharField(max_length=1)

#     class Meta:
#         managed = False
#         db_table = 'sales_deals'




# class Deposits(models.Model):
#     date = models.DateField()
#     deposit_number = models.BigIntegerField()
#     dhs = models.CharField(max_length=191)
#     fils = models.CharField(max_length=191)
#     cheque_no = models.CharField(max_length=191)
#     bank = models.CharField(max_length=191)
#     sec_date = models.DateField()
#     being = models.CharField(max_length=191)
#     status = models.CharField(max_length=191)
#     deal_type = models.CharField(max_length=191)
#     received_from = models.CharField(max_length=191, null=True, blank=True)
#     payment_type = models.CharField(max_length=191, null=True, blank=True)
#     deal_refer_no = models.CharField(max_length=191)
#     sum_of_dhs = models.CharField(max_length=191)
#     agent_name = models.CharField(max_length=191)
#     project_name = models.CharField(max_length=191)
#     building_name = models.CharField(max_length=191)
#     unit_number = models.CharField(max_length=191)
#     created_at = models.DateTimeField(null=True, blank=True)
#     updated_at = models.DateTimeField(null=True, blank=True)
#     account_id = models.IntegerField()
#     on_behalf_of = models.CharField(max_length=191)

#     def __str__(self):
#         return f"Deposit #{self.deposit_number} - {self.cheque_no}"
    
#     class Meta:
#         managed = False
#         db_table = 'deposits'