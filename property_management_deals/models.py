

from django.db import models
from django.contrib.auth.models import User
import uuid
import os

from datetime import datetime

def unique_upload_path(instance, filename, folder_name):
    ext = filename.split('.')[-1]
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    unique_id = uuid.uuid4().hex[:8]
    ref_number = getattr(instance, 'reference_number', 'unknown')
    new_filename = f"{ref_number}_{timestamp}_{unique_id}.{ext}"
    return os.path.join(f'uploads/{folder_name}/', new_filename)

def upload_to_pms_contract(instance, filename):
    return unique_upload_path(instance, filename, 'pms_contracts')

def upload_to_passport(instance, filename):
    return unique_upload_path(instance, filename, 'passports')

def upload_to_eid(instance, filename):
    return unique_upload_path(instance, filename, 'eid_copies')

def upload_to_cheque(instance, filename):
    return unique_upload_path(instance, filename, 'cheques')

def upload_to_title_deed(instance, filename):
    return unique_upload_path(instance, filename, 'title_deeds')

def upload_to_kyc_form(instance, filename):
    return unique_upload_path(instance, filename, 'kyc_forms')

def upload_to_screening(instance, filename):
    return unique_upload_path(instance, filename, 'screenings')

def upload_to_poa_pp(instance, filename):
    return unique_upload_path(instance, filename, 'poa_pps')

def upload_to_poa_copy(instance, filename):
    return unique_upload_path(instance, filename, 'poa_copies')

def upload_to_key_hand_over(instance, filename):
    return unique_upload_path(instance, filename, 'key_handovers')

class Receipt(models.Model):
    receipt_number = models.CharField(max_length=100)

    def __str__(self):
        return self.receipt_number

class Property(models.Model):
    # Agent Info
    agent_name = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False, related_name='properties')

    # Property Basic Details
    deal_date = models.DateField()
    reference_number = models.CharField(max_length=100, unique=True)
    project_name = models.CharField(max_length=100)
    building_name = models.CharField(max_length=100)
    unit_no = models.CharField(max_length=50)
    pms_price = models.DecimalField(max_digits=12, decimal_places=2)
    pm_start_date = models.DateField()
    pm_end_date = models.DateField()
    tenancy_start_date = models.DateField()
    tenancy_end_date = models.DateField()

    # Owner Details
    owner_name = models.CharField(max_length=100)
    owner_source = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='owner_sources')
    owner_mobile = models.CharField(max_length=20)
    owner_email = models.EmailField()
    seller_nationality = models.CharField(max_length=100)

    # Owner Agency Details
    #agency_name = models.CharField(max_length=100)
    agency_name = models.CharField(max_length=100, default='Default Agency')

    agent_brn = models.CharField(max_length=100, blank=True, null=True)
    agent_name_text = models.CharField(max_length=100,blank=False,null=True)
    agent_phone = models.CharField(max_length=20)
    agent_email = models.EmailField(blank=True, null=True)

    # Cheque Details
    number_of_cheques = models.PositiveIntegerField()
    cheque_date = models.DateField()

    # Revenue / Commission Details
    total_commission = models.DecimalField(max_digits=12, decimal_places=2)
    outside_commission = models.DecimalField(max_digits=12, decimal_places=2)
    net_commission = models.DecimalField(max_digits=12, decimal_places=2)
    classic = models.CharField(max_length=100)

    agent1 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='agent1_properties')
    # agent1_commission = models.DecimalField(max_digits=12, decimal_places=2)
    agent1_commission = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)



    agent2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='agent2_properties')
    agent2_commission = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    agent3 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='agent3_properties')
    agent3_commission = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    comment_by_agent = models.TextField(blank=True, null=True)
    comment_by_admin = models.TextField(blank=True, null=True)

    receipt = models.CharField(max_length=100, blank=True, null=True)
    kyc_number = models.CharField(max_length=100, blank=True, null=True)

    STATUS_CHOICES = [
        ('Accept', 'Accept'),
        ('Reject', 'Reject'),
        ('Pending', 'Pending'),
        ('Waiting for Finance', 'Waiting for Finance'),
    ]
    approval_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')

    AML_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    aml = models.CharField(max_length=10, choices=AML_CHOICES)
    # Required fields (with *) — mandatory uploads
    pms_contract = models.FileField(upload_to=upload_to_pms_contract, blank=False, null=False)
    owner_passport_copy = models.FileField(upload_to=upload_to_passport, blank=False, null=False)
    owner_eid_copy = models.FileField(upload_to=upload_to_eid, blank=False, null=False)
    pms_cheque_copy = models.FileField(upload_to=upload_to_cheque, blank=False, null=False)
    title_deed = models.FileField(upload_to=upload_to_title_deed, blank=False, null=False)
    kyc_form = models.FileField(upload_to=upload_to_kyc_form, blank=False, null=False)
    screening = models.FileField(upload_to=upload_to_screening, blank=False, null=False)

    poa_pp = models.FileField(upload_to=upload_to_poa_pp, blank=True, null=True)
    poa_copy = models.FileField(upload_to=upload_to_poa_copy, blank=True, null=True)
    key_hand_over_form = models.FileField(upload_to=upload_to_key_hand_over, blank=True, null=True)


    FORM_CHOICES = [ 
        ('Submitted', 'Submitted'), 
        ('Draft', 'Draft'), 
    ]

    Form_status = models.CharField(
        max_length=30,
        choices=FORM_CHOICES,
        default='Draft'
    )

    ENTERED_FINANCE = [
        ('True','True'),
        ('False','False'),
    ]

    is_entered_finance = models.CharField(max_length=30,choices=ENTERED_FINANCE,default='False')

    def __str__(self):
        return f"{self.reference_number} - {self.project_name}"

