from rest_framework import serializers
from core.models import RentalDeals,Users,Receipts
from rest_framework.reverse import reverse
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

# class RentalDealSingleFieldSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RentalDeals
#         fields = ['is_entered_in_finance_system']


class ReceiptDropdownSerilizer(serializers.ModelSerializer):

    class Meta :
        model = Receipts
        fields = ['id','receipt_number']

User = get_user_model()
class AgentDropdownSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ['id', 'name']

    def get_name(self, obj):
        return f"{obj.name}".strip()
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class DealSerializer(serializers.ModelSerializer):
    # users = UserSerializer(source='submitted_by_user', read_only=True)
    

    date = serializers.DateField(
        input_formats=["%d-%m-%Y"],   # Accept DMY from frontend
        format="%d-%m-%Y"             # Return DMY to frontend
    )
    deal_start_date = serializers.DateField(
        input_formats=["%d-%m-%Y"],   # Accept DMY from frontend
        format="%d-%m-%Y"             # Return DMY to frontend
    )
    deal_end_date = serializers.DateField(
        input_formats=["%d-%m-%Y"],   # Accept DMY from frontend
        format="%d-%m-%Y"             # Return DMY to frontend
    )


    reference_number = serializers.CharField(required=True)  # <-- manually define it!
    

    view_link = serializers.SerializerMethodField()
    update_link = serializers.SerializerMethodField()
    delete_link = serializers.SerializerMethodField()
    
    email = serializers.CharField(source='submitted_by_user.email', read_only=True)
    username = serializers.CharField(source = "submitted_by_user.name",read_only =True)

    is_approved_rejected_display = serializers.SerializerMethodField()
    manager_approved_rejected_display = serializers.SerializerMethodField()
    is_entered_in_finance_system_display = serializers.SerializerMethodField()



    class Meta:
        model = RentalDeals
        fields = '__all__'
        extra_fields = ['view_link', 'update_link', 'delete_link','agent_username']

    
    CONDITIONAL_REQUIRED_FIELDS = [
        'owner_agency',
        'agent_first_name',
        'agent_phone',
        'tenant_agency',
        'tenant_agent_first_name',
        'tenant_agent_phone',
        'tenancy_contract',           # Added from error output
        'owner_passport_copy',        # Added from error output
        'tenant_passport_visa_copy',  # Added from error output
        'rental_deposit_cheque_copy', # Added from error output
        'title_deed',                 # Added from error output
        'total_commission',
        'less_outsude_commission',
        'net_commission',
        'classic',
        'agent1',
        'receipt_no',
        'rental_kyc_number',          # Added from error output
        # Also ensure these are here if they apply:
        # 'is_sale_aml',
        'agent_name1',
        'is_rental_aml',
        # Any other fields that should only be required for 'Complete' status
    ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ On update, remove UniqueValidator for all fields
        if self.instance:
            for field in self.fields.values():
                field.validators = [
                    v for v in field.validators if not isinstance(v, UniqueValidator)
                ]
        
        # form_status = self.initial_data.get('form_status') 

      
        # form_status = data.get('form_status', 'Incomplete')

        if 'data' in kwargs: # Check if 'data' key exists in kwargs passed to serializer
            # Retrieve form_status only if data is present
            form_status = self.initial_data.get('form_status')
            print()
            print(f"DEBUG: Serializer validate method called. Data received: {form_status}") # <--- ADD THIS
            print()
            if form_status == 'Incomplete':
                print()
                print(f"DEBUG: form_status inside Incomplete: {form_status}") 
                print()
                # For draft, make fields in CONDITIONAL_REQUIRED_FIELDS not required
                for field_name in self.CONDITIONAL_REQUIRED_FIELDS:
                    if field_name in self.fields: # Check if the field actually exists in the serializer
                        self.fields[field_name].required = False

                        # Handle 'This field may not be blank.' errors for string fields
                        if isinstance(self.fields[field_name], serializers.CharField):
                            self.fields[field_name].allow_blank = True
                        # Handle 'This field may not be blank.' for fields that might be numeric or other types
                        # if they receive empty string, they might need allow_null=True or specific validation
                        # Note: Numeric fields receiving '' will likely error during type conversion unless allow_null=True
                        # or you explicitly handle empty strings in a custom field type.
                        elif isinstance(self.fields[field_name], (serializers.IntegerField,
                                                                serializers.FloatField,
                                                                serializers.DecimalField,
                                                                )): # Applies to ImageFields too
                            self.fields[field_name].allow_null = True
                            # You might also need to handle empty strings for numeric fields if they come from HTML forms
                            # by custom logic or by making the model field nullable/blank.
                            # For FileFields like 'tenancy_contract', 'owner_passport_copy', etc.,
                            # setting required=False and allow_null=True is the correct approach.

    # when edit ting the recored it thins as anew record creationto bypass that
    def validate_reference_number(self, value):
        qs = RentalDeals.objects.filter(reference_number=value)
        if self.instance:
            if self.instance.reference_number == value:
                return value
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("This reference number is already used.")
        return value

    def validate(self, data):
        form_status = data.get('form_status', 'Incomplete')
        print(f"DEBUG: Serializer validate method called. Data received: {data}") # <--- ADD THIS
        form_status = data.get('form_status', 'Incomplete')
        print(f"DEBUG: form_status inside serializer: {form_status}") 

        print()
        print("this is for the sermilser " ,form_status)
        print()

        # Required for saving as DRAFT
        if form_status == 'Incomplete':
            draft_required_fields = [
                'submitted_by_agent',
                'reference_number',
                'date',
                'is_new_deal',
                'project_name',
                'unit_details',
                'building_name',
                'deal_start_date',
                'deal_end_date',
                'owner_first_name',
                'owner_source',
                'owner_mobile',
                'owner_email',
                'seller_nationality',
                'buyer_nationality',
                'tenant_first_name',
                'tenant_source',
                'tenant_mobile',
                'tenant_email',
                'screening'
            ]
            missing_fields = [
                field for field in draft_required_fields if not data.get(field)
            ]
            if missing_fields:
                raise serializers.ValidationError({
                    field: "This field is required for saving as draft."
                    for field in missing_fields
                })

        # Required for final submission
        elif form_status == 'Complete':
            complete_required_fields = [
                'submitted_by_agent', 'owner_agency', 'reference_number', 'date', 'is_new_deal',
                'project_name', 'unit_details', 'building_name', 'deal_start_date', 'deal_end_date',
                'owner_first_name', 'owner_source', 'owner_mobile', 'owner_email',
                'seller_nationality', 'buyer_nationality', 'tenant_first_name', 'tenant_source',
                'tenant_mobile', 'tenant_email', 'agent_first_name', 'agent_phone',
                'tenant_agency', 'tenant_agent_first_name', 'tenant_agent_phone',
                'total_commission', 'less_outsude_commission', 'net_commission',
                'classic', 'agent1', 'receipt_no', 'is_sale_aml', 'agent_name1',
                'is_rental_aml', 'screening'
            ]
            missing_fields = [
                field for field in complete_required_fields if not data.get(field)
            ]
            if missing_fields:
                raise serializers.ValidationError({
                    field: "This field is required when submitting the form."
                    for field in missing_fields
                })

            # KYC validation (only for Complete)
            

        # Return validated data
        return data

    def get_view_link(self, obj): 
        request = self.context.get('request')
        
        print(request)
        
        if request:
            return reverse('rental-deal-view', kwargs={"pk":obj.pk},request=request)
        return None

    def get_update_link(self, obj):
        request = self.context.get('request')
        url = reverse('rental-deal-update', args=[obj.pk])
        if request:
            return request.build_absolute_uri(url)
        return url

    def get_delete_link(self, obj):
        request = self.context.get('request')
        url = reverse('rental-deal-delete', args=[obj.pk])
        if request:
            return request.build_absolute_uri(url)
        return url
    
    # to get the full form s of A,P,R,W  
    def get_is_approved_rejected_display(self, obj):
        return obj.get_is_approved_rejected_display()

    def get_manager_approved_rejected_display(self, obj):
        return obj.get_manager_approved_rejected_display()
    
    def get_is_entered_in_finance_system_display(self, obj):
        return obj.get_is_entered_in_finance_system_display()
    
    

        # extra_fields = ['agent_username'] 
        


    # def validate(self, data):
    #     """
    #     Enforce required fields only when status is 'submitted'.
    #     """
    #     status = data.get('status', self.instance.status if self.instance else 'draft')

    #     if status == 'submitted':
    #         required_fields = [
    #             'agent',
    #             'deal_date',
    #             'reference_number',
    #             'deal_type',
    #             'project_name',
    #             'unit_number',
    #             'building_name',
    #             'deal_start_date',
    #             'deal_end_date',
    #         ]

        #     missing = [field for field in required_fields if not data.get(field)]
        #     if missing:
        #         raise serializers.ValidationError({
        #             field: "This field is required when submitting." for field in missing
        #         })

        # return data  


class SearchSerializer(serializers.Serializer):
    value = serializers.CharField(required=False, allow_blank=True)
    regex = serializers.BooleanField(required=False, default=False)

class filterSerializer(serializers.Serializer):
    """
    Serializer for filtering Rental Deals.
    """

    start = serializers.IntegerField(required=False, default=0)
    length = serializers.IntegerField(required=False, default=10)
    draw = serializers.IntegerField(required=False, default=0)

    search =  SearchSerializer(required=False, default=dict)

    type = serializers.CharField(required=False, allow_blank=True)
    from_date = serializers.DateField(required=False,   input_formats=["%Y-%m-%d"], allow_null=True)
    to_date = serializers.DateField(required=False,   input_formats=["%Y-%m-%d"], allow_null=True)

    reference_number = serializers.CharField(required=False, allow_blank=True)
    unit_details = serializers.CharField(required=False, allow_blank=True)
    building_name = serializers.CharField(required=False, allow_blank=True)
    deal_type = serializers.CharField(required=False, allow_blank=True)
    deal_status = serializers.CharField(required=False, allow_blank=True)
    project_name = serializers.CharField(required=False, allow_blank=True)
    owner_name = serializers.CharField(required=False, allow_blank=True)
    tenant_name = serializers.CharField(required=False, allow_blank=True)
    owner_mobile = serializers.CharField(required=False, allow_blank=True)
    tenant_mobile = serializers.CharField(required=False, allow_blank=True)

    
     
             
        
