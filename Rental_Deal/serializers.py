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
    # submitted_date = serializers.DateField(read_only=True) 

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
    deal_start_date = serializers.DateField(
        input_formats=["%d-%m-%Y"],   # Accept DMY from frontend
        format="%d-%m-%Y"             # Return DMY to frontend
    )
    deal_end_date = serializers.DateField(
        input_formats=["%d-%m-%Y"],   # Accept DMY from frontend
        format="%d-%m-%Y"             # Return DMY to frontend
    )


    reference_number = serializers.CharField(required=True)  # <-- manually define it!
    

     
    contract_value = serializers.SerializerMethodField()

    email = serializers.CharField(source='submitted_by_user.email', read_only=True)
    username = serializers.CharField(source = "submitted_by_user.name",read_only =True)

    is_approved_rejected_display = serializers.SerializerMethodField()
    manager_approved_rejected_display = serializers.SerializerMethodField()
    is_entered_in_finance_system_display = serializers.SerializerMethodField()
    action = serializers.SerializerMethodField()
    agent_name1_display = serializers.SerializerMethodField()
    agent_name2_display = serializers.SerializerMethodField()
    agent_name3_display = serializers.SerializerMethodField()
    





    class Meta:
        model = RentalDeals
        fields = '__all__'
        extra_fields = ['agent_username','action' ,'agent_name1_display','agent_name2_display','agent_name3_display' ]

    
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
        qs = RentalDeals.objects.filter(reference_number=value , is_deleted='N')
        if self.instance:
            if self.instance.reference_number == value:
                return value
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("This reference number is already used.")
        return value

    # def validate(self, data):
    #     form_status = data.get('form_status', 'Incomplete')
    #     print(f"DEBUG: Serializer validate method called. Data received: {data}") # <--- ADD THIS
    #     form_status = data.get('form_status', 'Incomplete')
    #     print(f"DEBUG: form_status inside serializer: {form_status}") 

    #     print()
    #     print("this is for the sermilser " ,form_status)
    #     print()

    #     # Required for saving as DRAFT
    #     if form_status == 'Incomplete':
    #         draft_required_fields = [
    #             'submitted_by_agent',
    #             'reference_number',
    #             'date',
    #             'is_new_deal',
    #             'project_name',
    #             'unit_details',
    #             'building_name',
    #             'deal_start_date',
    #             'deal_end_date',
    #             'owner_first_name',
    #             'owner_source',
    #             'owner_mobile',
    #             'owner_email',
    #             'seller_nationality',
    #             'buyer_nationality',
    #             'tenant_first_name',
    #             'tenant_source',
    #             'tenant_mobile',
    #             'tenant_email',
               
    #         ]
    #         missing_fields = [
    #             field for field in draft_required_fields if not data.get(field)
    #         ]
    #         if missing_fields:
    #             raise serializers.ValidationError({
    #                 field: "This field is required for saving as draft."
    #                 for field in missing_fields
    #             })

    #     # Required for final submission
    #     elif form_status == 'Complete':
    #         complete_required_fields = [
    #             'submitted_by_agent', 'owner_agency', 'reference_number', 'date', 'is_new_deal',
    #             'project_name', 'unit_details', 'building_name', 'deal_start_date', 'deal_end_date',
    #             'owner_first_name', 'owner_source', 'owner_mobile', 'owner_email',
    #             'seller_nationality', 'buyer_nationality', 'tenant_first_name', 'tenant_source',
    #             'tenant_mobile', 'tenant_email', 'agent_first_name', 'agent_phone',
    #             'tenant_agency', 'tenant_agent_first_name', 'tenant_agent_phone',
    #             'total_commission', 'less_outsude_commission', 'net_commission',
    #             'classic', 'agent1', 'receipt_no',  'agent_name1'
                
    #         ]
    #         missing_fields = [
    #             field for field in complete_required_fields if not data.get(field)
    #         ]
    #         if missing_fields:
    #             raise serializers.ValidationError({
    #                 field: "This field is required when submitting the form."
    #                 for field in missing_fields
    #             })

    #         # KYC validation (only for Complete)
            

    #     # Return validated data
    #     return data

   
    
    # to get the full form s of A,P,R,W  
    def get_is_approved_rejected_display(self, obj):
        return obj.get_is_approved_rejected_display()

    def get_manager_approved_rejected_display(self, obj):
        return obj.get_manager_approved_rejected_display()
    
    def get_is_entered_in_finance_system_display(self, obj):
        return obj.get_is_entered_in_finance_system_display()


  
    

    def get_action(self, obj):
        request = self.context.get('request')
     
        user = request.user
        html = ""

        # View
        if user.has_perm('core.view_rentaldeals'):
            # print("it has view permission ifromteh  serlozer")
            html += f'<a href="/rental-deals/view/{obj.id}/" class="text-primary mr-2"><i class="fas fa-eye"></i></a>'

        # Edit (disallowed if approved unless special permission exists)
        if user.has_perm('core.change_rentaldeals'):
            # print("thsi is from  ifromnthe serlizer ", obj.is_approved_rejected =='A' )
            

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
        return self.number_to_international_words(obj.rental_price)


    def number_to_international_words(self, number):
        if not number:
            return "Invalid amount"

    # Convert to string and clean up
        number = str(number).upper().strip()

        # Remove currency codes and symbols (case-insensitive because of .upper())
        for symbol in ["AED", "USD", "$", "DHS", "DIRHAMS"]:
            number = number.replace(symbol, "")

        # Remove commas and spaces
        number = number.replace(",", "").strip()

        # Remove decimal part if any
        if "." in number:
            number = number.split(".")[0]

        # Validate
        if not number.isdigit():
            return "Invalid amount"

        number = int(number)
        if number == 0:
            return "Zero"

        ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
        teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen",
                "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
        tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
        thousands = ["", "Thousand", "Million", "Billion", "Trillion"]

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

        words = []
        group_index = 0

        while number > 0:
            group = number % 1000
            if group != 0:
                group_words = three_digits(group)
                if thousands[group_index]:
                    group_words += " " + thousands[group_index]
                words.insert(0, group_words.strip())
            number //= 1000
            group_index += 1

        return " ".join(words).strip()
    

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
        """
        Ensure reference_number is unique, even during update.
        """
        # If creating new record
        if self.instance is None:
            if RentalDeals.objects.filter(reference_number=value, is_deleted="N").exists():
                raise serializers.ValidationError("This reference number is already taken.")
        else:
            # Updating existing record — exclude current instance
            if RentalDeals.objects.exclude(pk=self.instance.pk).filter(reference_number=value).exists():
                raise serializers.ValidationError("This reference number is already taken.")
        return value

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
    owner_first_name = serializers.CharField(required=False, allow_blank=True)
    tenant_first_name = serializers.CharField(required=False, allow_blank=True)
    owner_mobile = serializers.CharField(required=False, allow_blank=True)
    tenant_mobile = serializers.CharField(required=False, allow_blank=True)
    is_approved_rejected = serializers.CharField(required=False, allow_blank=True)



class DealSerializerfordatatable(serializers.ModelSerializer):
    date = serializers.DateField(
        input_formats=["%d-%m-%Y"],   # Accept DMY from frontend
        format="%d-%m-%Y"             # Return DMY to frontend
    )
    submitted_date = serializers.DateField(
        input_formats=["%d-%m-%Y"],   # Accept DMY from frontend
        format="%d-%m-%Y",
          read_only=True            # Return DMY to frontend
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
    

     
     

    # email =  serializers.SerializerMethodField()
    email = serializers.CharField(source='submitted_by_user.email', read_only=True)
    username = serializers.CharField(source="submitted_by_user.name", read_only=True)
    agent_name1_display = serializers.SerializerMethodField()
    agent_name2_display = serializers.SerializerMethodField()
    agent_name3_display = serializers.SerializerMethodField()

    is_approved_rejected_display = serializers.SerializerMethodField()
    manager_approved_rejected_display = serializers.SerializerMethodField()
    is_entered_in_finance_system_display = serializers.SerializerMethodField()
    action = serializers.SerializerMethodField()



    class Meta:
        model = RentalDeals
        fields =   [
             "id",
        "submitted_date",
        "submitted_by_user",
        "reference_number",
        "date",
        "unit_details",
        "building_name",
        "project_name",
        "is_new_deal",
        "owner_title",
        "owner_first_name",
        "owner_last_name",
        "owner_source",
        "owner_mobile",
        "owner_email",
        "tenant_title",
        "tenant_first_name",
        "tenant_last_name",
        "tenant_source",
        "tenant_mobile",
        "tenant_email",
        "owner_agency",
        "agent_first_name",
        "agent_last_name",
        "agent_phone",
        "agent_email",
        "brn",
        "tenant_agency",
        "tenant_agent_first_name",
        "tenant_agent_last_name",
        "tenant_agent_phone",
        "tenant_agent_email",
        "tenant_brn",
        "tenancy_contract",
        "owner_passport_copy",
        "tenant_passport_visa_copy",
        "tenant_emirates_id",
        "rental_deposit_cheque_copy",
        "title_deed",
        "owner_poa_pp_copy",
        "key_hand_over_form",
        "total_commission",
        "less_outsude_commission",
        "net_commission",
        "classic",
        "agent1",
        "agent2",
        "agent3",
        "is_approved_rejected",
        "approved_rejected_by",
        "is_entered_in_finance_system",
        "comments",
        "rental_price",
        "ejari",
        "agent_name1",
        "agent_name2",
        "agent_name3",
        "owner_eid_copy",
        "agent_comment",
        "mediating_agency",
        "mediating_agent_name",
        "mediating_agent_phone",
        "mediating_agent_email",
        "mediating_agency_brn",
        "poa_copy",
        "deal_start_date",
        "deal_end_date",
        "receipt_no",
        "form_status",
        "rental_kyc_number",
        "is_rental_aml",
        "kyc_number",
        "comments_finance",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
        "account",
        "property",
        "is_deleted",
        "plot_no",
        "mode_of_payment",
        "deal_agent",
        "receipt_id",
        "property_usage",
        "property_size",
        "premises_no",
        "security_deposit",
        "submitted_by_agent",
        "property_type",
        "tenancy_application_form",
        "screening",
        "screening_comments",
        "seller_nationality",
        "buyer_nationality",
        "manager_approved_rejected",
            "email", "username","action",       
            "agent_name1_display",
            "agent_name2_display",
            "agent_name3_display",
            "is_approved_rejected_display",
            "manager_approved_rejected_display",
            "is_entered_in_finance_system_display"
            
        ]
        extra_fields = ['agent_username','action','agent_name1_display','agent_name2_display','agent_name3_display' ]


    def get_action(self, obj):
        request = self.context.get('request')
     
        user = request.user
        html = ""

        # View
        if user.has_perm('core.view_rentaldeals'):
            html += f'<a href="/rental-deals/view/{obj.id}/" class="text-primary mr-2"><i class="fas fa-eye"></i></a>'

        # Edit (disallowed if approved unless special permission exists)
        if user.has_perm('core.change_rentaldeals'):
            if obj.is_approved_rejected == "A" and (not user.has_perm('core.edit_approved_rental_deals')):
                html+=""
            else:
                html += f'<a href="/rental-deals/update/{obj.id}/" class="text-warning mx-2" id="editDealBtn" data-deal-id="{obj.id}"><i class="fas fa-edit"></i></a>'

        # Delete
        if user.has_perm('core.delete_rentaldeals'):
            html += f'<a href="#" class="text-danger delete-btn" data-id="{obj.id}" data-bs-toggle="modal" data-bs-target="#deleteModal"><i class="fas fa-trash"></i></a>'

        return format_html(html)
    

    def get_is_approved_rejected_display(self, obj):
        return obj.get_is_approved_rejected_display()

    def get_manager_approved_rejected_display(self, obj):
        return obj.get_manager_approved_rejected_display()
    
    def get_is_entered_in_finance_system_display(self, obj):
        return obj.get_is_entered_in_finance_system_display()
    
    def get_email(self, obj):
        """
        Fetches the agent name from the User table using the stored user ID.
        Returns None if the user doesn't exist.
        """
        try:
            user = Users.objects.get(id=obj.submitted_by_agent)
            return user.email
        except (Users.DoesNotExist, TypeError, ValueError):
            return None
        
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
    

    
    


    
     
             
        




