from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from core.models import SalesDeals,Users
from django.utils.html import format_html
from django.contrib.auth import get_user_model

User = get_user_model()
class SalesDealSerializer(serializers.ModelSerializer):
 
    email = serializers.CharField( source="submitted_by_user.email" ,read_only=True)
    username = serializers.CharField( source="submitted_by_user.name" ,read_only=True)
    action = serializers.SerializerMethodField()
    agent_name1_display = serializers.SerializerMethodField()
    agent_name2_display = serializers.SerializerMethodField()
    agent_name3_display = serializers.SerializerMethodField()

    # Making the required fields optional and allow blank
    reference_number = serializers.CharField(required=False, allow_blank=True, )
    unit_details = serializers.CharField(required=False, allow_blank=True)
    building_name = serializers.CharField(required=False, allow_blank=True)
    deal_status = serializers.CharField(required=False, allow_blank=True)
    project_name = serializers.CharField(required=False, allow_blank=True)
    screening_comments = serializers.CharField(required=False, allow_blank=True)
    date = serializers.DateField(
        input_formats=["%d-%m-%Y"],   # Accept DMY from frontend
        format="%d-%m-%Y"             # Return DMY to frontend
    )
    submitted_date = serializers.DateField(
        input_formats=["%d-%m-%Y"],   # Accept DMY from frontend
        format="%d-%m-%Y"             # Return DMY to frontend
    )

    class Meta:
        model = SalesDeals
        fields = '__all__'
        extra_fields = ['action','agent_name1_display','agent_name2_display','agent_name3_display']

    def get_action(self, obj):
        request = self.context.get('request')
     
        user = request.user
        html = ""

        # View
        if user.has_perm('core.view_salesdeals'):
            # print("it has view permission ifromteh  serlozer")
            html += f'<a href="/sales-deals/view/{obj.id}/" class="text-primary mr-2"><i class="fas fa-eye"></i></a>'

        # Edit (disallowed if approved unless special permission exists)
        if user.has_perm('core.change_salesdeals'):
            
            

            if obj.is_approved_rejected == "A" and (not user.has_perm('core.edit_approved_sales_deals')):
                print("entered the edit ")
                html+=""

            else:
                html += f'<a href="/sales-deals/{obj.id}/edit/" class="text-warning mx-2" id="editDealBtn" data-deal-id="{obj.id}"><i class="fas fa-edit"></i></a>'

        # Delete
        if user.has_perm('core.delete_salesdeals'):
            html += f'<a href="#" class="text-danger delete-btn" data-id="{obj.id}" data-bs-toggle="modal" data-bs-target="#deleteModal"><i class="fas fa-trash"></i></a>'

        return format_html(html)
    

    def get_agent_name1_display(self, obj):
        try:
            if not obj.agent_name1 :
                return ""
            user = User.objects.get(id=obj.agent_name1)
            return user.get_full_name() or user.name
        except User.DoesNotExist:
            return None
        
    def get_agent_name2_display(self, obj):
        try:
            if not obj.agent_name2 :
                return ""
            user = User.objects.get(id=obj.agent_name2)
            return user.get_full_name() or user.name
        except User.DoesNotExist:
            return None
        
    def get_agent_name3_display(self, obj):
        try:
            if not obj.agent_name3 :
                return ""
            user = User.objects.get(id=obj.agent_name3)
            return user.get_full_name() or user.name
        except User.DoesNotExist:
            return None
    def validate_reference_number(self, value):
        qs = SalesDeals.objects.filter(reference_number=value , is_deleted='N')
        if self.instance:
            if self.instance.reference_number == value:
                return value
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("This reference number is already used.")
        return value




class filterSerializer(serializers.Serializer):
    draw = serializers.IntegerField(required=False)
    start = serializers.IntegerField(required=False, default=0)
    length = serializers.IntegerField(required=False, default=10)

    search = serializers.DictField(required=False)

    reference_number = serializers.CharField(required=False, allow_blank=True)
    unit_details = serializers.CharField(required=False, allow_blank=True)
    builduing_name = serializers.CharField(required=False, allow_blank=True)
    deal_type = serializers.CharField(required=False, allow_blank=True)
    deal_status = serializers.CharField(required=False, allow_blank=True)
    project_name = serializers.CharField(required=False, allow_blank=True)
    buyer_name = serializers.CharField(required=False, allow_blank=True)
    buyer_source = serializers.CharField(required=False, allow_blank=True)
     
    owner_mobile = serializers.CharField(required=False, allow_blank=True)
    buyer_mobile = serializers.CharField(required=False, allow_blank=True)
    seller_mobile = serializers.CharField(required=False, allow_blank=True)
    seller_name = serializers.CharField(required=False, allow_blank=True)
    seller_source = serializers.CharField(required=False, allow_blank=True)
    is_approved_rejected = serializers.CharField(required=False, allow_blank=True)

    from_date = serializers.DateField(required=False)
    to_date = serializers.DateField(required=False)

    type = serializers.CharField(required=False, allow_blank=True)


class AgentDropdownSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ['id', 'name']

    def get_name(self, obj):
        return f"{obj.name}".strip()
    




class SalesDealSerializerForDraft(serializers.ModelSerializer):
    # Override only the required fields to make them optional
    agent1 = serializers.DecimalField(required=False, allow_null=True, max_digits=10, decimal_places=2)
    buyer_agency = serializers.CharField(required=False, allow_blank=True)
    buyer_agent_name = serializers.CharField(required=False, allow_blank=True)
    buyer_agent_phone = serializers.CharField(required=False, allow_blank=True)
    classic = serializers.DecimalField(required=False, allow_null=True, max_digits=10, decimal_places=2)
    less_outside_commission = serializers.CharField(required=False, allow_blank=True)
     
    net_commission = serializers.DecimalField(required=False, allow_null=True, max_digits=10, decimal_places=2)
    receipt_no = serializers.CharField(required=False, allow_blank=True)
    seller_agency = serializers.CharField(required=False, allow_blank=True)
    seller_agent_name = serializers.CharField(required=False, allow_blank=True)
    seller_agent_phone = serializers.CharField(required=False, allow_blank=True)
    total_commission = serializers.DecimalField(required=False, allow_null=True, max_digits=10, decimal_places=2)
    less_outsude_commission = serializers.CharField(required=False, allow_blank=True)
    screening_comments = serializers.CharField(required=False, allow_blank=True)
    

    date = serializers.DateField(
        input_formats=["%d-%m-%Y"],   # Accept DMY from frontend
        format="%d-%m-%Y"             # Return DMY to frontend
    )
    submitted_date = serializers.DateField(
        input_formats=["%d-%m-%Y"],   # Accept DMY from frontend
        format="%d-%m-%Y",
        required=False,  # make it optional
        allow_null=True              # Return DMY to frontend
    )


    class Meta:
        model = SalesDeals
        fields = '__all__'

    def validate_reference_number(self, value):
        qs = SalesDeals.objects.filter(reference_number=value , is_deleted='N')
        if self.instance:
            if self.instance.reference_number == value:
                return value
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("This reference number is already used.")
        return value






class salesdealSerilizerforNon_file_validation(serializers.ModelSerializer):
    # Override only the required fields to make them optional
    agent1 = serializers.DecimalField(required=False, allow_null=True, max_digits=10, decimal_places=2)
    buyer_agency = serializers.CharField(required=False, allow_blank=True)
    buyer_agent_name = serializers.CharField(required=False, allow_blank=True)
    buyer_agent_phone = serializers.CharField(required=False, allow_blank=True)
    classic = serializers.DecimalField(required=False, allow_null=True, max_digits=10, decimal_places=2)
    less_outside_commission = serializers.CharField(required=False, allow_blank=True)
    net_commission = serializers.DecimalField(required=False, allow_null=True, max_digits=10, decimal_places=2)
    receipt_no = serializers.CharField(required=False, allow_blank=True)
    seller_agency = serializers.CharField(required=False, allow_blank=True)
    seller_agent_name = serializers.CharField(required=False, allow_blank=True)
    seller_agent_phone = serializers.CharField(required=False, allow_blank=True)
    total_commission = serializers.DecimalField(required=False, allow_null=True, max_digits=10, decimal_places=2)
    less_outsude_commission = serializers.CharField(required=False, allow_blank=True)
    screening_comments = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = SalesDeals
        fields = '__all__'
        exclude = []


# Serializer for data table with action field
class SalesDealSerializerFordatafilter(serializers.ModelSerializer):

    email = serializers.CharField( source="submitted_by_user.email" ,read_only=True)
    username = serializers.CharField(source="submitted_by_user.name", read_only=True)
    action = serializers.SerializerMethodField()

    # display agent names for the three agents
    agent_name1_display = serializers.SerializerMethodField()
    agent_name2_display = serializers.SerializerMethodField()
    agent_name3_display = serializers.SerializerMethodField()

    # display approved/rejected status
    is_approved_rejected_display = serializers.SerializerMethodField() 
    manager_approved_rejected_display =serializers.SerializerMethodField()
    is_entered_in_finance_system_display =serializers.SerializerMethodField()


    class Meta:
        model = SalesDeals
        fields = ["id",
    "account_id",
    "reference_number",
      # if you have this field in your model

    # Deal info
    "date",                     # Deal Date
    "submitted_date",           # Submission / Start Date
    "deal_amount",              # Deal Amount / Rental Price
    "project_name",
    "builduing_name",
    "unit_details",

    # Approval / status info
    "form_status",
    "manager_approved_rejected",
    "is_approved_rejected",
    "approved_rejected_by",
    "is_deleted",

    # Submitted by user (related table)
    "submitted_by_user",
    

    # Owner (Seller) info
    "seller_name",
    "seller_source",
    "selller_mobile",
    "seller_email",
    "seller_nationality",
    "seller_agency",
    "seller_agent_name",
    "seller_agent_phone",
    "seller_agent_email",
    "seller_agency_brn",

    # Tenant (Buyer) info
    "buyer_name",
    "buyer_source",
    "buyer_mobile",
    "buyer_email",
    "buyer_nationality",
    "buyer_agency",
    "buyer_agent_name",
    "buyer_agent_phone",
    "buyer_agent_email",
    "buyer_agency_brn",

    # Mediating agency info
    "mediating_agency",
    "mediating_agent_name",
    "mediating_agent_phone",
    "mediating_agent_email",
    "mediating_agency_brn",

    # Commission info
    "total_commission",
    "less_outsude_commission",
    "net_commission",
    "classic",
    "agent1",
    "agent2",
    "agent3",
    "agent_name1",
    "agent_name2",
    "agent_name3",

    # Finance info
    "receipt_no",
    "kyc_number",
    "is_sale_aml",
    "is_entered_in_finance_system",

    # Comments & metadata
    "comments",
    "agent_comment",
    "comments_finance",
    "created_at",
    "created_by",
    "updated_by",
    "action","email","deal_amount","username","agent_name1_display","agent_name2_display","agent_name3_display","is_approved_rejected_display","manager_approved_rejected_display","is_entered_in_finance_system_display"]
        
    def get_action(self, obj):
        request = self.context.get('request')
     
        user = request.user
        html = ""

        # View
        if user.has_perm('core.view_salesdeals'):
            # print("it has view permission ifromteh  serlozer")
            html += f'<a href="/sales-deals/view/{obj.id}/" class="text-primary mr-2"><i class="fas fa-eye"></i></a>'

        # Edit (disallowed if approved unless special permission exists)
        if user.has_perm('core.change_salesdeals'):
            
            

            if obj.is_approved_rejected == "A" and (not user.has_perm('core.edit_approved_sales_deals')):
                print("entered the edit approved in serlizer ")
                html+=""

            else:
                html += f'<a href="/sales-deals/{obj.id}/edit/" class="text-warning mx-2" id="editDealBtn" data-deal-id="{obj.id}"><i class="fas fa-edit"></i></a>'

        # Delete
        if user.has_perm('core.delete_salesdeals'):
            html += f'<a href="#" class="text-danger delete-btn" data-id="{obj.id}" data-bs-toggle="modal" data-bs-target="#deleteModal"><i class="fas fa-trash"></i></a>'

        return format_html(html)
    
    # display agent names for the three agents
    
    def get_agent_name1_display(self, obj):
        try:
            if not obj.agent_name1 :
                return ""
            user = User.objects.get(id=obj.agent_name1)
            return user.get_full_name() or user.name
        except User.DoesNotExist:
            return None
        
    def get_agent_name2_display(self, obj):
        try:
            if not obj.agent_name2 :
                return ""
            user = User.objects.get(id=obj.agent_name2)
            return user.get_full_name() or user.name
        except User.DoesNotExist:
            return None
        
    def get_agent_name3_display(self, obj):
        try:
            if not obj.agent_name3 :
                return ""
            user = User.objects.get(id=obj.agent_name3)
            return user.get_full_name() or user.name
        except User.DoesNotExist:
            return None
    
    # dispaly the  approved and rejected statusof the deals 
    def get_is_approved_rejected_display(self, obj):
        return obj.get_is_approved_rejected_display()

    def get_manager_approved_rejected_display(self, obj):
        return obj.get_manager_approved_rejected_display()
    
    def get_is_entered_in_finance_system_display(self, obj):
        return obj.get_is_entered_in_finance_system_display()

