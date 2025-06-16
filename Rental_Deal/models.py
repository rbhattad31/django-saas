from datetime import date
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import uuid

# Create your models here.
  


class RentalDeals(models.Model):
    id = models.BigAutoField(primary_key=True)
    submitted_date = models.DateField()
    submitted_by_user = models.ForeignKey('Users', models.DO_NOTHING)
    reference_number = models.TextField()
    date = models.DateField()
    unit_details = models.TextField()
    building_name = models.TextField()
    project_name = models.TextField()
    is_new_deal = models.CharField(max_length=1)
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
    is_approved_rejected = models.CharField(max_length=1)
    approved_rejected_by = models.TextField(blank=True, null=True)
    is_entered_in_finance_system = models.BooleanField(default=False)
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
    form_status = models.CharField(max_length=10, blank=True, null=True)
    rental_kyc_number = models.TextField()
    is_rental_aml = models.CharField(max_length=3, blank=True, null=True)
    kyc_number = models.TextField(blank=True, null=True)
    comments_finance = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=191, blank=True, null=True)
    updated_by = models.CharField(max_length=191, blank=True, null=True)
    account = models.ForeignKey('Accounts', models.DO_NOTHING, blank=True, null=True)
    property = models.ForeignKey('Properties', models.DO_NOTHING, blank=True, null=True)
    # branch = models.ForeignKey('Branches', models.DO_NOTHING, blank=True, null=True)
    is_deleted = models.CharField(max_length=1)
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
    manager_approved_rejected = models.CharField(max_length=1)


   

    class Meta:
        managed = False
        db_table = 'rental_deals'


class Accounts(models.Model):
    id = models.BigAutoField(primary_key=True)
    account_name = models.CharField(unique=True, max_length=191)
    account_domain = models.CharField(unique=True, max_length=191)
    contact_name = models.CharField(max_length=191, blank=True, null=True)
    contact_email = models.CharField(max_length=191, blank=True, null=True)
    contact_phone = models.CharField(max_length=191, blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    logo = models.TextField(blank=True, null=True)
    plan = models.CharField(max_length=191, blank=True, null=True)
    max_users = models.CharField(max_length=191, blank=True, null=True)
    min_users = models.CharField(max_length=191, blank=True, null=True)
    is_active = models.CharField(max_length=1)
    is_deleted = models.CharField(max_length=1)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=191, blank=True, null=True)
    updated_by = models.CharField(max_length=191, blank=True, null=True)
    is_approved = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'accounts'



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    

    def get_by_natural_key(self, email):
        return self.get(email=email)


class Users(AbstractBaseUser,PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=191,blank=False, null=True)
    mobile_number = models.CharField(max_length=191)
    role = models.IntegerField()
    email = models.CharField(unique=True, max_length=191)
    password = models.CharField(max_length=191)
    gender = models.CharField(max_length=6, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    timezone = models.CharField(max_length=191, blank=True, null=True)
    is_active = models.CharField(max_length=1)
    is_deleted = models.CharField(max_length=1)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    last_login = models.DateTimeField(
    db_column='last_login_date_time', blank=True, null=True
)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=191)
    updated_by = models.CharField(max_length=191, blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    user_account_id = models.CharField(max_length=191)

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}"
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','password']

    class Meta:
        managed = False
        db_table = 'users'


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
    


 


 

 






