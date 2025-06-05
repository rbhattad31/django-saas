from datetime import date
from django.db import models
import uuid

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Commission Detail Model

 
    # total_commission = models.DecimalField(max_digits=10, decimal_places=2)
    # less_outside_commission = models.DecimalField(max_digits=10, decimal_places=2)
    # net_commission = models.DecimalField(max_digits=10, decimal_places=2)
    # classic = models.CharField(max_length=100)

    # # Agents and their commission splits
    # agent1 = models.ForeignKey(User, related_name='agent1_commissions', on_delete=models.SET_NULL, null=True, blank=True)
    # agent1_commission = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # agent2 = models.ForeignKey(User, related_name='agent2_commissions', on_delete=models.SET_NULL, null=True, blank=True)
    # agent2_commission = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # agent3 = models.ForeignKey(User, related_name='agent3_commissions', on_delete=models.SET_NULL, null=True, blank=True)
    # agent3_commission = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # # Comments
    # comment_by_agent = models.TextField(null=True, blank=True)
    # comment_by_admin = models.TextField(null=True, blank=True)

    # receipt_no = models.CharField(max_length=100)
    # kyc_number = models.CharField(max_length=100, null=True, blank=True)

    
    # aml = models.CharField(max_length=3, choices=AML_CHOICES)

 
    # approval_status = models.CharField(max_length=20, choices=APPROVAL_CHOICES,null=True)

    # created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"Commission #{self.id} - Receipt {self.receipt_no}"

# Rental Deal  Rental_Deals    Model
class Rental_Deal(models.Model):
    DEAL_TYPE_CHOICES = [
        ('new', 'New'),
        ('renewal', 'Renewal'),
    ]
    APPROVAL_CHOICES = (
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('waiting', 'Waiting for Finance'),
    )
    AML_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )

    PROPERTY_USAGE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        # Add more as needed
    ]

    

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
    ]

    # Required Fields
    # Relation to User model for agent
    
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='deals')  # Required via serializer logic
    # Relation to Owner model for property owner
    # owner = models.ForeignKey('Owner', on_delete=models.CASCADE, related_name='rental_deals')
    deal_date = models.DateField(default=date.today)
    reference_number = models.CharField(max_length=100, unique=True)
    deal_type = models.CharField(max_length=10, choices=DEAL_TYPE_CHOICES) 
    project_name = models.CharField(max_length=200)
    unit_number = models.CharField(max_length=50)
    building_name = models.CharField(max_length=200)
    deal_start_date = models.DateField()
    deal_end_date = models.DateField()

    # Optional Fields
    property_usage = models.CharField(max_length=50, choices=PROPERTY_USAGE_CHOICES, blank=True, null=True)
    property_type = models.CharField(max_length=50, blank=True, null=True)
    property_size = models.CharField(max_length=50, blank=True, null=True)
    rental_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    security_deposit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    mode_of_payment = models.CharField(max_length=100, blank=True, null=True)
    premises_number = models.CharField(max_length=50, blank=True, null=True)
    plot_number = models.CharField(max_length=50, blank=True, null=True)

    # Save as Draft / Submit Handling
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

 
   
 
    #source Details
    owner_name = models.CharField(max_length=100)
    owner_mobile = models.CharField(max_length=20)
    owner_nationality = models.CharField(max_length=50)
    owner_email = models.EmailField()
    # source = models.ForeignKey('OwnerSource', on_delete=models.SET_NULL, null=True, blank=True)

 

    tenant_name = models.CharField(max_length=100)
    tenant_mobile = models.CharField(max_length=20)
    tenant_nationality = models.CharField(max_length=50)
    tenant_email = models.EmailField()



    # Agency Details

    owner_agency_name = models.CharField(max_length=255)
    owner_agency_brn = models.CharField(max_length=100, blank=True, null=True)
    owner_agent_name = models.CharField(max_length=255)
    owner_agent_phone = models.CharField(max_length=20)
    owner_agent_email = models.EmailField(blank=True, null=True)

    # Tenant Agency
    tenant_agency_name = models.CharField(max_length=255)
    tenant_agency_brn = models.CharField(max_length=100, blank=True, null=True)
    tenant_agent_name = models.CharField(max_length=255)
    tenant_agent_phone = models.CharField(max_length=20)
    tenant_agent_email = models.EmailField(blank=True, null=True)

    # Mediating Agency
    mediating_agency_name = models.CharField(max_length=255, blank=True, null=True)
    mediating_agency_brn = models.CharField(max_length=100, blank=True, null=True)
    mediating_agent_name = models.CharField(max_length=255, blank=True, null=True)
    mediating_agent_phone = models.CharField(max_length=20, blank=True, null=True)
    mediating_agent_email = models.EmailField(blank=True, null=True)

    # Revenue Details
    total_commission = models.DecimalField(max_digits=10, decimal_places=2)
    less_outside_commission = models.DecimalField(max_digits=10, decimal_places=2)
    net_commission = models.DecimalField(max_digits=10, decimal_places=2)
    classic = models.CharField(max_length=100)


   
    # Agents and their commission splits
    agent1 = models.ForeignKey(User, related_name='agent1_commissions', on_delete=models.SET_NULL, null=True, blank=True)
    agent1_commission = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    agent2 = models.ForeignKey(User, related_name='agent2_commissions', on_delete=models.SET_NULL, null=True, blank=True)
    agent2_commission = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    agent3 = models.ForeignKey(User, related_name='agent3_commissions', on_delete=models.SET_NULL, null=True, blank=True)
    agent3_commission = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Comments
    comment_by_agent = models.TextField(null=True, blank=True)
    comment_by_admin = models.TextField(null=True, blank=True)

    receipt_no = models.CharField(max_length=100)
    kyc_number = models.CharField(max_length=100, null=True, blank=True)

    AML_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )
    aml = models.CharField(max_length=3, choices=AML_CHOICES)

    APPROVAL_CHOICES = (
        ('pending', 'Pending'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('waiting', 'Waiting for Finance'),
    )
    approval_status = models.CharField(max_length=20, choices=APPROVAL_CHOICES,default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    is_entered_finance = models.BooleanField(default=False)

    # documents
 

    tenancy_contract = models.FileField(upload_to=f'documents/tenancy_contracts/{uuid.uuid4()}/', blank=True, null=True)
    title_deed = models.FileField(upload_to=f'documents/title_deeds/{uuid.uuid4()}/', blank=True, null=True)
    tenant_passport_visa_copy = models.FileField(upload_to=f'documents/tenant_passports/{uuid.uuid4()}/', blank=True, null=True)
    owner_eid_copy = models.FileField(upload_to=f'documents/owner_eid/{uuid.uuid4()}/', blank=True, null=True)
    poa_pp = models.FileField(upload_to=f'documents/poa_pp/{uuid.uuid4()}/', blank=True, null=True)
    key_handover_form = models.FileField(upload_to=f'documents/key_handover/{uuid.uuid4()}/', blank=True, null=True)
    tenancy_application_form = models.FileField(upload_to=f'documents/tenancy_applications/{uuid.uuid4()}/', blank=True, null=True)

    owner_passport_copy = models.FileField(upload_to=f'documents/owner_passports/{uuid.uuid4()}/', blank=True, null=True)
    ejari = models.FileField(upload_to=f'documents/ejari/{uuid.uuid4()}/', blank=True, null=True)
    tenants_eid_copy = models.FileField(upload_to=f'documents/tenant_eid/{uuid.uuid4()}/', blank=True, null=True)
    rental_deposit_rental_cheque_copy = models.FileField(upload_to=f'documents/cheques/{uuid.uuid4()}/', blank=True, null=True)
    poa_copy = models.FileField(upload_to=f'documents/poa_copy/{uuid.uuid4()}/', blank=True, null=True)
    kyc_form = models.FileField(upload_to=f'documents/kyc_forms/{uuid.uuid4()}/', blank=True, null=True)
    screening = models.FileField(upload_to=f'documents/screenings/{uuid.uuid4()}/', blank=True, null=True)

    screening_comments = models.TextField(blank=True, null=True)
 
    




 
# 
 


 

 






