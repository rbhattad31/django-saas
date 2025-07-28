from rest_framework import serializers
from core.models import RentalDeals,Users,Receipts
from django.utils.html import format_html
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
        fields = ['id', 'name',"email"]

    def get_name(self, obj):
        return f"{obj.name}".strip()
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class DealSerializer(serializers.ModelSerializer):
    # is_rental_aml = serializers.CharField(required=False, allow_null=True, allow_blank=True)
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
    contract_value = serializers.SerializerMethodField()

    email = serializers.CharField(source='submitted_by_user.email', read_only=True)
    username = serializers.CharField(source = "submitted_by_user.name",read_only =True)

    is_approved_rejected_display = serializers.SerializerMethodField()
    manager_approved_rejected_display = serializers.SerializerMethodField()
    is_entered_in_finance_system_display = serializers.SerializerMethodField()
    action = serializers.SerializerMethodField()



    class Meta:
        model = RentalDeals
        fields = '__all__'
        extra_fields = ['view_link', 'update_link', 'delete_link','agent_username','action']

    
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
                'classic', 'agent1', 'receipt_no',  'agent_name1',
                  'screening'
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


    can_edit = serializers.SerializerMethodField()
    can_delete = serializers.SerializerMethodField()
    can_view = serializers.SerializerMethodField()

    def get_can_view(self, obj):
        # obj is the RentalDeal instance for the current row
        request = self.context.get('request')
        if not request:
            return False # No request context, cannot determine permissions

        # Example: User must have 'change_rentaldeal' permission and deal must not be 'archived'
        # Replace 'your_app.change_rentaldeal' with your actual permission string
        has_permission = request.user.has_perm('core.view_rentaldeals')
        # is_editable_status = obj.status != 'archived' # Example status check

        return has_permission  

    

    def get_can_edit(self, obj):
        # obj is the RentalDeal instance for the current row
        request = self.context.get('request')
        if not request:
            return False # No request context, cannot determine permissions

        # Example: User must have 'change_rentaldeal' permission and deal must not be 'archived'
        # Replace 'your_app.change_rentaldeal' with your actual permission string
        has_permission = request.user.has_perm('core.change_rentaldeals')
        # is_editable_status = obj.status != 'archived' # Example status check

        return has_permission  

    def get_can_delete(self, obj):
        # obj is the RentalDeal instance for the current row
        request = self.context.get('request')
        if not request:
            return False # No request context, cannot determine permissions

        # Example: User must have 'delete_rentaldeal' permission and be the creator of the deal
        # Replace 'your_app.delete_rentaldeal' with your actual permission string
        has_permission = request.user.has_perm('core.delete_rentaldeals')
        # is_owner = (request.user == obj.created_by) if obj.created_by else False # Assuming created_by is a User field

        return has_permission  
    

    def get_action(self, obj):
        request = self.context.get('request')
     
        user = request.user
        html = ""

        # View
        if user.has_perm('core.view_rentaldeals'):
            print("it has view permission ifromteh  serlozer")
            html += f'<a href="/rental-deals/view/{obj.id}/" class="text-primary mr-2"><i class="fas fa-eye"></i></a>'

        # Edit (disallowed if approved unless special permission exists)
        if user.has_perm('core.change_rentaldeals'):
            print("thsi is from  ifromnthe serlizer ", obj.is_approved_rejected =='A' )
            print(type(obj.is_approved_rejected))
            print("thsi is from  ifromnthe serlizer ", user.has_perm('core.edit_approved_rental_deals')  )

            if obj.is_approved_rejected == "A" and (not user.has_perm('core.edit_approved_rental_deals')):
                print("entered the edit ")
                html+=""

            else:
                html += f'<a href="/rental-deals/update/{obj.id}/" class="text-warning mx-2" id="editDealBtn" data-deal-id="{obj.id}"><i class="fas fa-edit"></i></a>'

        # Delete
        if user.has_perm('core.delete_rentaldeals'):
            html += f'<a href="#" class="text-danger delete-btn" data-id="{obj.id}" data-bs-toggle="modal" data-bs-target="#deleteModal"><i class="fas fa-trash"></i></a>'

        return format_html(html)
    
    
    def get_contract_value(self, obj):
        print(obj , "thisis objet for serlizer")
        return self.number_to_indian_words(obj.rental_price)


    def number_to_indian_words(self, number):
        print(number ,'the amount number ')

        if not number:
            return "Invalid amount"

    # Remove commas and extra spaces
        number = str(number).replace(",", "").strip()

        if not number.isdigit():
            return "Invalid amount"
        
        number = int(number)
        ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
        teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen",
                 "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
        tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]

        def two_digits(n):
            if 10 <= n <= 19:
                return teens[n - 10]
            elif n >= 20:
                return tens[n // 10] + (" " + ones[n % 10] if n % 10 != 0 else "")
            else:
                return ones[n]

        def three_digits(n):
            if n == 0:
                return ""
            elif n < 100:
                return two_digits(n)
            else:
                return ones[n // 100] + " Hundred" + (" " + two_digits(n % 100) if n % 100 != 0 else "")

        if number == 0:
            return "Zero"
        if number > 99999999:
            return "Number exceeds 1 crore"

        parts = []
        crore = number // 10000000
        if crore:
            parts.append(ones[crore] + " Crore")
        number %= 10000000

        lakh = number // 100000
        if lakh:
            parts.append(two_digits(lakh) + " Lakh")
        number %= 100000

        thousand = number // 1000
        if thousand:
            parts.append(two_digits(thousand) + " Thousand")
        number %= 1000

        hundred_and_below = three_digits(number)
        if hundred_and_below:
            parts.append(hundred_and_below)

        return " ".join(parts)

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

    
     
             
        
