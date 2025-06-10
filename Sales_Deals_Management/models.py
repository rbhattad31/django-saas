from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SalesDeal(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted','submitted'),
        
    ]

    deal_submitted_by_agent = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True)
    reference_number = models.CharField(max_length=50, unique=True, blank=False)
    submitted_date = models.DateField(blank=False)
    unit_no = models.CharField(max_length=20, blank=False)
    building_name = models.CharField(max_length=100, blank=False)
    project_name = models.CharField(max_length=100, blank=False)
    selling_price = models.DecimalField(max_digits=15, decimal_places=2, blank=False)

    # Seller details
    seller_name = models.CharField(max_length=255, blank=False, null=True)
    seller_mobile = models.CharField(max_length=20, blank=False, null=True)
    seller_email = models.EmailField(blank=False, null=True)
    seller_nationality = models.CharField(max_length=100, blank=False, null=True)
    seller_source = models.CharField(max_length=255, blank=False, null=True)

    # Buyer details
    buyer_name = models.CharField(max_length=100, blank=False, null=True)
    buyer_mobile = models.CharField(max_length=20, blank=False, null=True)
    buyer_email = models.EmailField(blank=False, null=True)
    buyer_nationality = models.CharField(max_length=100, blank=False, null=True)
    buyer_source = models.CharField(max_length=255, blank=False, null=True)

    # Seller Agency
    seller_agency_name = models.CharField(max_length=255, blank=False, null=True)
    seller_agency_brn = models.CharField(max_length=100, blank=True, null=True)
    seller_agent_name = models.CharField(max_length=255, blank=False, null=True)
    seller_agent_phone = models.CharField(max_length=20, blank=False, null=True)
    seller_agent_email = models.EmailField(blank=True, null=True)

    # Buyer Agency
    buyer_agency_name = models.CharField(max_length=255, blank=False, null=True)
    buyer_agency_brn = models.CharField(max_length=100, blank=True, null=True)
    buyer_agent_name = models.CharField(max_length=255, blank=False, null=True)
    buyer_agent_phone = models.CharField(max_length=20, blank=False, null=True)
    buyer_agent_email = models.EmailField(blank=True, null=True)

    # Mediating Agency
    mediating_agency_name = models.CharField(max_length=255, blank=False, null=True)
    mediating_agency_brn = models.CharField(max_length=100, blank=True, null=True)
    mediating_agent_name = models.CharField(max_length=255, blank=False, null=True)
    mediating_agent_phone = models.CharField(max_length=20, blank=False, null=True)
    mediating_agent_email = models.EmailField(blank=True, null=True)

    # New Financial Fields
    total_commission = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=True)
    net_commission = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=True)
    less_outside_commission = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=True)
    classic = models.CharField(max_length=101, blank=False, null=True)

    # Agent Commission Info
    agent1 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='agent1_deals', null=True, blank=False)
    agent1_commission = models.DecimalField(max_digits=12, decimal_places=2, blank=False,null=True)

    agent2 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='agent2_deals', null=True, blank=True)
    agent2_commission = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    agent3 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='agent3_deals', null=True, blank=True)
    agent3_commission = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # Comments & Tracking
    comment_by_agent = models.TextField(blank=True, null=True)
    comment_by_admin = models.TextField(blank=True, null=True)
    receipt_no = models.CharField(max_length=100, blank=False,null=True)
    kyc_number = models.CharField(max_length=100, blank=True, null=True)

    aml = models.BooleanField(default=False)

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='draft')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Upload Documents
    form_f = models.FileField(upload_to='documents/', blank=False, null=True)
    old_title_deed = models.FileField(upload_to='documents/', blank=False, null=True)
    owner_eid = models.FileField(upload_to='documents/', blank=True, null=True)
    buyers_deposit_cheque_copy = models.FileField(upload_to='documents/', blank=False, null=True)
    sellers_deposit_cheque_copy = models.FileField(upload_to='documents/', blank=True, null=True)
    buyer_poa_passport_copy = models.FileField(upload_to='documents/', blank=True, null=True)
    sellers_poa_copy = models.FileField(upload_to='documents/', blank=True, null=True)
    sellers_poa_eid = models.FileField(upload_to='documents/', blank=True, null=True)
    screening = models.FileField(upload_to='documents/', blank=False, null=True)
    manager_cheque_copy = models.FileField(upload_to='documents/', blank=False, null=True)

    new_title_deed = models.FileField(upload_to='documents/', blank=False, null=True)
    owners_passport_copy = models.FileField(upload_to='documents/', blank=False, null=True)
    buyers_passport_copy = models.FileField(upload_to='documents/', blank=False, null=True)
    buyer_eid = models.FileField(upload_to='documents/', blank=True, null=True)
    seller_poa_passport_copy = models.FileField(upload_to='documents/', blank=True, null=True)
    buyer_poa_copy = models.FileField(upload_to='documents/', blank=True, null=True)
    buyer_poa_eid = models.FileField(upload_to='documents/', blank=True, null=True)
    kyc_or_approval_form = models.FileField(upload_to='documents/', blank=True, null=True)

    screening_comments = models.TextField(blank=True, null=True)
    APPROVAL_STATUS_CHOICES = [
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('waiting_finance', 'Waiting for Finance'),
    ]

    approval_status = models.CharField(max_length=30, choices=APPROVAL_STATUS_CHOICES, default='waiting_finance')


    class Meta:
        ordering = ['-submitted_date']

    def __str__(self):
        return f"{self.reference_number} - {self.building_name}"
