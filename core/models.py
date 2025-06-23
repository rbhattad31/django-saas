# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser

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


# class Account(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     account_name = models.CharField(max_length=191, unique=True)
#     account_domain = models.CharField(max_length=191, unique=True)
#     contact_name = models.CharField(max_length=191, null=True, blank=True)
#     contact_email = models.CharField(max_length=191, null=True, blank=True)
#     contact_phone = models.CharField(max_length=191, null=True, blank=True)
#     additional_info = models.TextField(null=True, blank=True)
#     logo = models.TextField(null=True, blank=True)
#     plan = models.CharField(max_length=191, null=True, blank=True)
#     max_users = models.CharField(max_length=191, null=True, blank=True)
#     min_users = models.CharField(max_length=191, null=True, blank=True)
#     is_active = models.CharField(max_length=1, default='N')
#     is_deleted = models.CharField(max_length=1, default='N')
#     created_at = models.DateTimeField(null=True, blank=True)
#     updated_at = models.DateTimeField(null=True, blank=True)
#     created_by = models.CharField(max_length=191, null=True, blank=True)
#     updated_by = models.CharField(max_length=191, null=True, blank=True)
#     is_approved = models.CharField(max_length=1, default='N')

#     class Meta:
#         db_table = 'accounts'
#         managed = False

#     def __str__(self):
#         return self.account_name


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


# class Deposits(models.Model):
#     id = models.BigAutoField(primary_key=True)
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
#     on_behalf_of = models.CharField(max_length=191)

#     class Meta:
#         managed = False
#         db_table = 'deposits'


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


# class Receipts(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     date = models.DateField()
#     receipt_number = models.BigIntegerField()
#     dhs = models.CharField(max_length=191)
#     fils = models.CharField(max_length=191)
#     cheque_no = models.CharField(max_length=191)
#     bank = models.CharField(max_length=191)
#     sec_date = models.DateField()
#     being = models.CharField(max_length=191)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
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
#     account_id = models.IntegerField()
#     agent_id = models.IntegerField()
#     agent_email = models.CharField(max_length=255)
#     mail_status = models.CharField(max_length=255)

#     class Meta:
#         managed = False
#         db_table = 'receipts'





# class RentalProperties(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     deal_date = models.TextField()
#     reference_number = models.TextField()
#     pms = models.TextField()
#     project_name = models.TextField()
#     building_name = models.TextField()
#     unit_details = models.TextField()
#     pms_price = models.TextField()
#     pm_start_date = models.TextField()
#     pm_end_date = models.TextField()
#     tenancy_start_date = models.TextField()
#     tenancy_end_date = models.TextField()
#     owner_first_name = models.TextField()
#     owner_source = models.TextField()
#     owner_mobile = models.TextField()
#     owner_email = models.TextField()
#     agency_name = models.TextField()
#     agent_name = models.TextField()
#     brn = models.TextField(blank=True, null=True)
#     agent_phone = models.TextField()
#     agent_email = models.TextField(blank=True, null=True)
#     no_of_cheque = models.TextField()
#     cheque_date = models.TextField()
#     pms_contract = models.TextField()
#     owner_passport_copy = models.TextField()
#     owner_eid_copy = models.TextField()
#     pms_cheque_copy = models.TextField()
#     title_deed = models.TextField()
#     poa_pp = models.TextField(blank=True, null=True)
#     poa_copy = models.TextField(blank=True, null=True)
#     key_hand_over_form = models.TextField(blank=True, null=True)
#     kyc_form = models.TextField(blank=True, null=True)
#     kyc_number = models.TextField(blank=True, null=True)
#     total_commission = models.TextField()
#     less_outside_commission = models.TextField()
#     net_commission = models.TextField()
#     classic = models.TextField()
#     agent1 = models.TextField()
#     agent2 = models.TextField(blank=True, null=True)
#     agent3 = models.TextField(blank=True, null=True)
#     comments = models.TextField(blank=True, null=True)
#     agent_name1 = models.TextField(blank=True, null=True)
#     agent_name2 = models.TextField(blank=True, null=True)
#     agent_name3 = models.TextField(blank=True, null=True)
#     receipt_no = models.TextField()
#     form_status = models.CharField(max_length=10, blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     created_by = models.CharField(max_length=191, blank=True, null=True)
#     updated_by = models.CharField(max_length=191, blank=True, null=True)
#     account = models.ForeignKey(Account, models.DO_NOTHING, blank=True, null=True)
#     status = models.CharField(max_length=15)
#     deal_sno = models.IntegerField()
#     is_approved_rejected = models.CharField(max_length=1)
#     approved_rejected_by = models.TextField(blank=True, null=True)
#     is_entered_in_finance_system = models.CharField(max_length=1)
#     comments_finance = models.TextField(blank=True, null=True)
#     submitted_by_user_id = models.IntegerField()
#     is_deleted = models.CharField(max_length=1)
#     agent_comment = models.TextField(blank=True, null=True)
#     is_property_aml = models.CharField(max_length=3)
#     screening = models.CharField(max_length=191)
#     screening_comments = models.TextField()
#     seller_nationality = models.CharField(max_length=191)
#     buyer_nationality = models.CharField(max_length=191)
#     submitted_date = models.DateField()
#     manager_approved_rejected = models.CharField(max_length=1)

#     class Meta:
#         managed = False
#         db_table = 'rental_properties'



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


# class SalesDeals(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     submitted_date = models.DateField()
#     submitted_by_user = models.ForeignKey('Users', models.DO_NOTHING)
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
#     account = models.ForeignKey(Account, models.DO_NOTHING, blank=True, null=True)
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
         
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # extra_fields.setdefault('role', Role.objects.get(id=1))
        
        
        return self.create_user(email, password, **extra_fields)


class Users(AbstractBaseUser,PermissionsMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=191, blank=False, null=True)
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
    user_account_id = models.IntegerField(null=True,blank=True , default=2)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
     


    # djagno searche sfor Lastlogin but ue are using diff filed so make it present but not in DB
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

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

from django.db import models

class RentalDeals(models.Model):
    submitted_date = models.DateField()
    submitted_by_user = models.ForeignKey('users', on_delete=models.CASCADE)
    reference_number = models.TextField()
    date = models.DateField()
    unit_details = models.TextField()
    building_name = models.TextField()
    project_name = models.TextField()
    is_new_deal = models.CharField(max_length=1, choices=[('R', 'R'), ('Y', 'Y'), ('N', 'N')], default='Y')
    owner_title = models.TextField(blank=True, null=True)
    owner_first_name = models.TextField()
    owner_last_name = models.TextField(blank=True, null=True)
    owner_source = models.TextField()
    owner_mobile = models.TextField()
    owner_email = models.TextField(blank=True, null=True)
    tenant_title = models.TextField()
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
    is_approved_rejected = models.CharField(max_length=1, choices=[('P', 'P'), ('F', 'F'), ('A', 'A'), ('R', 'R')], default='P')
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
    form_status = models.CharField(max_length=10, choices=[('Complete', 'Complete'), ('Incomplete', 'Incomplete')], blank=True, null=True)
    rental_kyc_number = models.TextField()
    is_rental_aml = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], blank=True, null=True)
    kyc_number = models.TextField(blank=True, null=True)
    comments_finance = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=191, blank=True, null=True)
    updated_by = models.CharField(max_length=191, blank=True, null=True)
    account_id = models.IntegerField(null=True, blank=True ,default = 2 )
    property = models.ForeignKey('properties', on_delete=models.SET_NULL, blank=True, null=True)
    #branch = models.ForeignKey('branches', on_delete=models.SET_NULL, blank=True, null=True)
    is_deleted = models.CharField(max_length=1, choices=[('Y', 'Y'), ('N', 'N')], default='N')
    plot_no = models.TextField(blank=True, null=True)
    mode_of_payment = models.TextField(blank=True, null=True)
    deal_agent = models.CharField(max_length=191, blank=True, null=True)
    receipt_id = models.IntegerField()
    property_usage = models.CharField(max_length=191)
    property_size = models.CharField(max_length=191)
    premises_no = models.CharField(max_length=191)
    security_deposit = models.CharField(max_length=191)
    submitted_by_agent = models.IntegerField()
    property_type = models.CharField(max_length=191, blank=True, null=True)
    tenancy_application_form = models.CharField(max_length=191, blank=True, null=True)
    screening = models.CharField(max_length=191)
    screening_comments = models.TextField()
    seller_nationality = models.CharField(max_length=191)
    buyer_nationality = models.CharField(max_length=191)
    manager_approved_rejected = models.CharField(max_length=1, choices=[('P', 'P'), ('A', 'A'), ('R', 'R')], default='P')


    class Meta:
        #managed = False
        db_table = 'rental_deals'