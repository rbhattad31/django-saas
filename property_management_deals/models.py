from django.db import models

#this import files related to custom user logic
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission


#custom user imports completed.



#Custom user related classes.
# class CustomUserManager(BaseUserManager):
#     # def create_user(self, email, username, password=None, **extra_fields):
#     #     if not email:
#     #         raise ValueError(_('The Email field must be set'))
#     #     email = self.normalize_email(email)
#     #     user = self.model(email=email, **extra_fields)
#     #     user.set_password(password)
#     #     user.save(using=self._db)
#     #     return user
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError(_('The Email field must be set'))
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         #extra_fields.setdefault('role', 'admin')  # Default role for superuser

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError(_('Superuser must have is_staff=True.'))
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError(_('Superuser must have is_superuser=True.'))

#         return self.create_user(email, password, **extra_fields)

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     ROLE_CHOICES = (
#         ('agent', 'Agent'),
#         ('finance', 'Finance'),
#         ('admin', 'Admin'),
#         ('manager', 'Manager'),
#     )

#     email = models.EmailField(_('email address'), unique=True)
#     username = models.CharField(max_length=150, unique=True)
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='agent')
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     class Meta:
#         db_table = 'custom_users'

#     def __str__(self):
#         return self.email

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
#     is_deleted = models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')], default='N')

#     # is_deleted = models.BooleanField(default=False)

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

# #custom user class ended.

# class Accounts(models.Model):
#     id = models.BigAutoField(primary_key=True)
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
#         #managed = False
#         db_table = 'accounts'

#     # class Meta:
#     #     db_table = 'accounts'
#     #     managed = False

#     def __str__(self):
#         return self.account_name
   
    
#     def save(self, *args, **kwargs):
#         is_new = self.pk is None  # Check if the account is being created for the first time
#         super().save(*args, **kwargs)  # Save the Accoun

#     # Default Django permissions (CRUD)   
#         if is_new:
#             roles = {
#                 "Admin": [
#                     "add_rentalproperties",
#                     "property_rentalproperties",
#                     "draft_rentalproperties",  

#                     "create_draft_property_rentalproperties",
#                     "view_properties_rentalproperties",
#                     "edit_properties_rentalproperties",
#                     "delete_properties_rentalproperties",
#                     "edit_approved_properties_rentalproperties",

#                     "add_management_receipts_rentalproperties",
#                     "edit_management_receipts_rentalproperties",
#                     "view_management_receipts_rentalproperties",
#                     "download_management_receipts_rentalproperties",

#                     "pending_properties_rentalproperties",
#                     "approved_properties_rentalproperties",
#                     "rejected_properties_rentalproperties",
#                     "waiting_for_finance_properties_rentalproperties",
#                     "pending_finance_properties_rentalproperties",
#                     "entered_finance_properties_rentalproperties",

#                     "admin_properties_fields_rentalproperties",
#                     "update_aml_status_properties_rentalproperties",
#                     "update_finance_status_properties_rentalproperties",
#                     "finance_comment_properties_rentalproperties",
#                 ],

#                 "Manager": [
#                     "draft_rentalproperties",
#                     "view_properties_rentalproperties",
                    
#                     "edit_properties_rentalproperties",

#                     "view_management_receipts_rentalproperties",
#                     "download_management_receipts_rentalproperties",

#                     "pending_properties_rentalproperties",
#                     "approved_properties_rentalproperties",
#                     "rejected_properties_rentalproperties",
#                 ],

#                 "Agent": [
#                     "property_rentalproperties",
#                     "draft_rentalproperties",
#                     "add_rentalproperties",
#                     "create_draft_property_rentalproperties",
#                     "view_properties_rentalproperties",
#                     "edit_properties_rentalproperties",

#                     "pending_properties_rentalproperties",
#                     "approved_properties_rentalproperties",
#                     "rejected_properties_rentalproperties",
#                 ],

#                 "Finance": [
#                     "add_rentalproperties",
#                     "view_properties_rentalproperties",
#                     "add_management_receipts_rentalproperties",
#                     "edit_management_receipts_rentalproperties",
#                     "view_management_receipts_rentalproperties",
#                     "download_management_receipts_rentalproperties",

#                     "waiting_for_finance_properties_rentalproperties",
#                     "pending_finance_properties_rentalproperties",
#                     "entered_finance_properties_rentalproperties",

#                     "update_aml_status_properties_rentalproperties",
#                     "update_finance_status_properties_rentalproperties",
#                     "finance_comment_properties_rentalproperties",
#                 ]
#             }

#             for role, permissions in roles.items():
#                 group_name = f"{self.id}-{role}"
#                 group, _ = Group.objects.get_or_create(name=group_name)

#                 for codename in permissions:
#                     try:
#                         perm = Permission.objects.get(codename=codename)
#                         group.permissions.add(perm)
#                     except Permission.DoesNotExist:
#                         print(f"⚠️ Permission '{codename}' not found — please make sure it exists.")
        

# class RentalProperties(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     deal_date = models.TextField()
#     reference_number = models.TextField()
#     pms = models.TextField(blank= True , null = True)
    
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
#     # pms_contract = models.FileField(upload_to='uploads/', null=True, blank=True)
#     # owner_passport_copy = models.FileField(upload_to='uploads/', null=True, blank=True)
#     # owner_eid_copy = models.FileField(upload_to='uploads/', null=True, blank=True)
#     # pms_cheque_copy = models.FileField(upload_to='uploads/', null=True, blank=True)
#     # title_deed = models.FileField(upload_to='uploads/', null=True, blank=True)
#     # poa_pp = models.FileField(upload_to='uploads/', null=True, blank=True)
#     # poa_copy = models.FileField(upload_to='uploads/', null=True, blank=True)
#     # key_hand_over_form = models.FileField(upload_to='uploads/', null=True, blank=True)
#     # kyc_form = models.FileField(upload_to='uploads/', null=True, blank=True)
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
#     form_status = models.CharField(
#         max_length=50,
#         choices=[
#             ('Complete', 'Complete'),
#             ('Incomplete', 'Incomplete')
#         ],
#         blank=True,
#         null=True
#     )
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     created_by = models.CharField(max_length=191, blank=True, null=True)
#     updated_by = models.CharField(max_length=191, blank=True, null=True)
#     account = models.ForeignKey(Accounts, models.DO_NOTHING, blank=True, null=True)
      

#     status = models.CharField(max_length=20, choices = [
#         ('Active', 'Active'),
#         ('About To Expire', 'About To Expire'),
#         ('Expired', 'Expired'),
#         ('Renew', 'Renew'),
#         ('Closed', 'Closed'),
#         ('Inactive', 'Inactive'),
#     ], default='Active')
#     # deal_sno = models.IntegerField()
#     deal_sno = models.IntegerField(null=True,blank=True)
#     #is_approved_rejected = models.CharField(max_length=1)
#     # is_approved_rejected = models.CharField(max_length=1, null=False, blank=True)
#     is_approved_rejected = models.CharField(max_length=1,choices=[('P','pending'),("A","Approved"),('R',"Rejected"),('W',"Waiting Finance")] ,  null=True, blank=True,default="P")

#     approved_rejected_by = models.TextField(blank=True, null=True)
#     is_entered_in_finance_system = models.CharField(max_length=1)
#     comments_finance = models.TextField(blank=True, null=True)
#     submitted_by_user_id = models.IntegerField()
#     is_deleted = models.CharField(max_length=1,choices=[('Y','Y'),('N','N')],default='N')
#     agent_comment = models.TextField(blank=True, null=True)
#     is_property_aml = models.CharField(max_length=3)
#     screening = models.CharField(max_length=191)
#     screening_comments = models.TextField()
#     seller_nationality = models.CharField(max_length=191)
#     buyer_nationality = models.CharField(max_length=191)
#     submitted_date = models.DateField()
#     #manager_approved_rejected = models.CharField(max_length=10)
#     manager_approved_rejected = models.CharField(
#         max_length=1,
#         choices=[
#             ('A', 'Approved'),
#             ('R', 'Rejected'),
#             ('P', 'Pending'),
            
#         ],
#         null=True,
#         blank=True, default ="P"
#     )

#     class Meta:
#         #managed = False
#         db_table = 'rental_properties'

#     def debug_form_status(self):
#         print(f"\nForm Status: {self.form_status} (Length: {len(self.form_status) if self.form_status else 0})")


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
# class ManagementReceipts(models.Model):
#     id = models.BigAutoField(primary_key=True)  # 1. Primary Key, Auto Increment, NOT NULL
#     date = models.DateField(null=False)  # 2. NOT NULL
#     receipt_number = models.BigIntegerField(null=True,blank=True)  # 3. NOT NULL
#     dhs = models.CharField(max_length=191, null=False)  # 4. NOT NULL
#     fils = models.CharField(max_length=191, null=False)  # 5. NOT NULL
#     cheque_no = models.CharField(max_length=15, blank=True, null=True)  # 6. NOT NULL
#     # bank = models.CharField(max_length=191, null=False)  # 7. NOT NULL
#     bank = models.CharField(max_length=255, blank=True, null=True)
#     sec_date = models.DateField(null=False)  # 8. NOT NULL
#     being = models.CharField(max_length=191, null=False)  # 9. NOT NULL
#     status = models.CharField(max_length=191, null=False)  # 10. NOT NULL
#     # deal_type = models.CharField(max_length=191, null=False)  # 11. NOT NULL
#     deal_type = models.CharField(max_length=50, choices=[
#         ('Management Fee', 'Management Fee'),
#         ('Ejari Fee', 'Ejari Fee')
#     ])
#     received_from = models.CharField(max_length=191, blank=True, null=True)  # 12. DEFAULT NULL
#     # payment_type = models.CharField(max_length=191, blank=True, null=True)  # 13. DEFAULT NULL
#     payment_type = models.CharField(max_length=50, choices=[
#         ('Cash', 'Cash'),
#         ('Cheque', 'Cheque'),
#         ('Bank Transfer', 'Bank Transfer')
#     ])
#     deal_refer_no = models.CharField(max_length=191, null=True,blank=True)  # 14. NOT NULL
#     sum_of_dhs = models.CharField(max_length=191, null=False)  # 15. NOT NULL
#     agent_name = models.CharField(max_length=191, null=False)  # 16. NOT NULL
#     project_name = models.CharField(max_length=191, null=False)  # 17. NOT NULL
#     building_name = models.CharField(max_length=191, null=False)  # 18. NOT NULL
#     unit_number = models.CharField(max_length=191, null=False)  # 19. NOT NULL
#     created_at = models.DateTimeField(blank=True, null=True)  # 20. DEFAULT NULL
#     updated_at = models.DateTimeField(blank=True, null=True)  # 21. DEFAULT NULL
#     # account_id = models.IntegerField(null=False)  # 22. NOT NULL
#     account_id = models.IntegerField(null=True)  # 22. NOT NULL


#     class Meta:
#         managed = False  # Assuming this model is managed outside of Django (existing DB table)
#         db_table = 'management_receipts'

    

