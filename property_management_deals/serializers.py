 


from rest_framework import serializers
from core.models import RentalProperties,Users,ManagementReceipts
from django.contrib.auth import get_user_model
from datetime import date, datetime
import re
from django.db.models import Q
from core.models import RentalProperties, Account as Accounts
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

    def validate_is_deleted(self, value):
        if not value or value not in ['Y', 'N']:
            return 'N'
        return value

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if 'is_deleted' not in data or not data['is_deleted']:
            data['is_deleted'] = 'N'
        return data


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalProperties
        fields = '__all__'

    can_edit = serializers.SerializerMethodField()
    can_delete = serializers.SerializerMethodField()
    can_view = serializers.SerializerMethodField()
    can_edit_approved = serializers.SerializerMethodField()
 
    def get_can_view(self, obj):
        # obj is the RentalDeal instance for the current row
        request = self.context.get('request')
        if not request:
            print("enter data ")
            return False # No request context, cannot determine permissions
 
        
        has_permission = request.user.has_perm('core.view_properties_rentalproperties') 
        return has_permission  
 
   
 
    def get_can_edit(self, obj):
        # obj is the RentalDeal instance for the current row
        request = self.context.get('request')
        if not request:
            return False # No request context, cannot determine permissions
 
        # Example: User must have 'change_rentaldeal' permission and deal must not be 'archived'
        # Replace 'your_app.change_rentaldeal' with your actual permission string
        has_permission = request.user.has_perm('core.edit_properties_rentalproperties')
        # is_editable_status = obj.status != 'archived' # Example status check
 
        return has_permission  
 
    def get_can_delete(self, obj):
        # obj is the RentalDeal instance for the current row
        request = self.context.get('request')
        if not request:
            return False # No request context, cannot determine permissions
 
        # Example: User must have 'delete_rentaldeal' permission and be the creator of the deal
        # Replace 'your_app.delete_rentaldeal' with your actual permission string
        has_permission = request.user.has_perm('core.delete_properties_rentalproperties')
        # is_owner = (request.user == obj.created_by) if obj.created_by else False # Assuming created_by is a User field
 
        return has_permission  
    
    def get_can_edit_approved(self,obj):
        request = self.context.get('request')
        if not request:
            return False # No request context, cannot determine permissions
        
        has_permission = request.user.has_perm('core.edit_approved_properties_rentalproperties')
        return has_permission
   
 
 
 

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
    type = serializers.CharField(required=False, allow_blank=True)
    search = SearchSerializer(required=False, default=dict)
    print("Search item:",search)

    
    building_name = serializers.CharField(required=False, allow_blank=True)
    project_name = serializers.CharField(required=False, allow_blank=True)
    
    deal_date = serializers.DateField(
        required=False,
        input_formats=["%d-%m-%Y", "%Y-%m-%d"],
        allow_null=True,
    )


    submitted_date = serializers.DateField(
        required=False,
        input_formats=["%d-%m-%Y", "%Y-%m-%d"],  # day-month-year format
        allow_null=True,
    )

    pm_start_date = serializers.DateField(
        required=False,
        input_formats=["%d-%m-%Y"],  # day-month-year format
        allow_null=True,
    )

    pm_end_date = serializers.DateField(
        required=False,
        input_formats=["%d-%m-%Y"],  # day-month-year format
        allow_null=True,
    )

    tenancy_start_date = serializers.DateField(
        required=False,
        input_formats=["%d-%m-%Y"],  # day-month-year format
        allow_null=True,
    )
    tenancy_end_date = serializers.DateField(
        required=False,
        input_formats=["%d-%m-%Y"],
        allow_null=True,
    )

    unit_details = serializers.CharField(required=False, allow_blank=True, default='')
    approval_status = serializers.CharField(required=False, allow_blank=True, default='')
    status = serializers.CharField(required=False, allow_blank=True, default='')
    reference_number = serializers.CharField(required=False, allow_blank=True, default='')
    # property_id = serializers.CharField(required=False, allow_blank=True, default='')
    id = serializers.CharField(required=False, allow_blank=True, default='') # this is for property id



class PropertySerializer(serializers.ModelSerializer):
 
   
 
    def __init__(self, *args, **kwargs):
        # Pop 'draft' from kwargs; default False
        self.draft = kwargs.pop('draft', False)
        super().__init__(*args, **kwargs)
 
        if self.draft:
            # Allow blank for fields that are mandatory in full form, but optional in draft
                draft_optional_fields = [
                    'agency_name', 'agent_name', 'agent_phone', 'total_commission',
                    'less_outside_commission', 'net_commission', 'classic', 'agent1'
                ]
                for field in draft_optional_fields:
                    if field in self.fields:
                        self.fields[field].required = False
                        self.fields[field].allow_blank = True
                        self.fields[field].allow_null = True
    receipt_no = serializers.CharField(required=False, allow_blank=True, allow_null=True)
 
    account_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    def validate_account_id(self, value):
        """
        Validate account_id, inferring from request.user.account.id if not provided.
        """
        if value is None:
            request = self.context.get('request')
            if request and request.user.is_authenticated and hasattr(request.user, 'account') and request.user.account:
                value = request.user.account.id
            else:
                raise serializers.ValidationError("Account ID is required and cannot be determined.")
       
        try:
            value = int(value)  # Ensure it's an integer
        except (TypeError, ValueError):
            raise serializers.ValidationError("Account ID must be a valid integer.")
       
        if not Accounts.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Account ID {value} does not exist.")
       
        return value
    submitted_by_agent = serializers.IntegerField(
        source='submitted_by_user_id',
        required=False,
        allow_null=True
    )
 
    # Read-only name display
    submitted_by_agent_name = serializers.SerializerMethodField()
 
    def get_submitted_by_agent_name(self, obj):
        if obj.submitted_by_user_id:
            try:
                return Users.objects.get(id=obj.submitted_by_user_id).name
            except Users.DoesNotExist:
                return None
        return None
 
    def validate_is_approved_rejected(self, value):
        # If field is empty, return "P"
        if not value:
            return "P"
        return value
 
    is_property_aml = serializers.ChoiceField(
        choices=[("Yes", "Yes"), ("No", "No")],
        required=False,   # not required for draft
        allow_blank=True
    )
    is_deleted = serializers.ChoiceField(
        choices=[('Y', 'Yes'), ('N', 'No')],
        default='N',
        allow_blank=False
    )
    is_approved_rejected = serializers.ChoiceField(
        choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected'), ('F', 'Waiting Finance')],
        default='P',
        allow_blank=False,
        required=False
    )
    is_entered_in_finance_system = serializers.ChoiceField(
        choices=[('0', 'No'), ('1', 'Yes')],
        default='0',
        allow_blank=False,
        required=False
    )
 
    owner_eid_copy = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    screening_comments = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    deal_date = serializers.CharField(max_length=10, required=False, allow_blank=True, allow_null=True)
    pm_start_date = serializers.CharField(max_length=10, required=False, allow_blank=True, allow_null=True)
    pm_end_date = serializers.CharField(max_length=10, required=False, allow_blank=True, allow_null=True)
    tenancy_start_date = serializers.CharField(max_length=10, required=False, allow_blank=True, allow_null=True)
    tenancy_end_date = serializers.CharField(max_length=10, required=False, allow_blank=True, allow_null=True)
    cheque_date = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    no_of_cheque = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    # cheque_date = serializers.CharField(
    #     child=serializers.DateField(format='%d-%m-%Y', input_formats=['%d-%m-%Y', '%Y-%m-%d', '%d-%m-%y']),
    #     allow_empty=True
    # )
    manager_approved_rejected = serializers.ChoiceField(
        choices=[('A', 'Approved'), ('R', 'Rejected')],
        required=False
    )
    pms_contract = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    owner_passport_copy = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    pms_cheque_copy = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    title_deed = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    kyc_form = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    # screening = serializers.CharField(required=False, allow_blank=True, allow_null=True)
 
   
   
    # def to_internal_value(self, data):
    #     if 'cheque_date' in data and isinstance(data['cheque_date'], str):
    #         print(f"to_internal_value: Received cheque_date: {data['cheque_date']}")
    #         try:
    #             import json
    #             cheque_dates = json.loads(data['cheque_date'])
    #             if not isinstance(cheque_dates, list):
    #                 raise ValueError("cheque_date must be a list")
    #             data = data.copy()
    #             # data['cheque_date'] = [str(item).strip() for item in cheque_dates if str(item).strip()]
    #             print(f"to_internal_value: Parsed cheque_date to list: {data['cheque_date']}")
    #         except (json.JSONDecodeError, ValueError):
    #             # Fallback to space-separated string
    #             parts = data['cheque_date'].strip().split()
    #             cleaned_parts = [part for part in parts if part.strip()]
    #             data = data.copy()
    #             data['cheque_date'] = cleaned_parts
    #             print(f"to_internal_value: Fallback - Converted cheque_date to list: {cleaned_parts}")
    #     return super().to_internal_value(data)
    def to_internal_value(self, data):
        if 'cheque_date' in data and isinstance(data['cheque_date'], str):
            print(f"to_internal_value: Received cheque_date: {data['cheque_date']}")
            # Normalize extra spaces
            cheque_date_str = " ".join(data['cheque_date'].split())
           
            # Optional: validate each date in the string
            accepted_formats = ["%Y-%m-%d", "%d-%m-%Y", "%d-%m-%y"]
            dates = cheque_date_str.split()
            formatted_dates = []
            for date_str in dates:
                for fmt in accepted_formats:
                    try:
                        parsed_date = datetime.strptime(date_str, fmt)
                        formatted_dates.append(parsed_date.strftime("%d-%m-%Y"))
                        break
                    except ValueError:
                        continue
                else:
                    raise serializers.ValidationError(
                        {"cheque_date": f"Invalid date format: '{date_str}'"}
                    )
           
            # Join back as a single string separated by space
            data = data.copy()
            data['cheque_date'] = " ".join(formatted_dates)
            print(f"to_internal_value: Normalized cheque_date string: {data['cheque_date']}")
       
        return super().to_internal_value(data)
 
 
       
    def validate_cheque_date(self, value):
        cleaned_dates = []
 
        if isinstance(value, str):
            # Split string by space, comma, semicolon, or pipe
            parts = re.split(r'[,;|\s]+', value.strip())
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                try:
                    parsed = datetime.strptime(part, "%d-%m-%Y")
                    cleaned_dates.append(parsed.strftime("%d-%m-%Y"))
                except ValueError:
                    try:
                        parsed = datetime.strptime(part, "%Y-%m-%d")
                        cleaned_dates.append(parsed.strftime("%d-%m-%Y"))
                    except ValueError:
                        raise serializers.ValidationError(f"Invalid date format: '{part}'")
            # Join dates with space instead of returning a list
            normalized_str = " ".join(cleaned_dates)
            print(normalized_str, "normalized cheque_date")
            return normalized_str
 
        elif isinstance(value, list):
            for v in value:
                if isinstance(v, (date, datetime)):
                    cleaned_dates.append(v.strftime('%d-%m-%Y'))
                elif isinstance(v, str) and v.strip():
                    cleaned_dates.append(v.strip())
            normalized_str = " ".join(cleaned_dates)
            print(normalized_str, "normalized cheque_date from list")
            return normalized_str
 
        elif isinstance(value, (date, datetime)):
            return value.strftime('%d-%m-%Y')
 
        raise serializers.ValidationError("Invalid format for cheque_date.")
 
 
   
   
    def create(self, validated_data):
        #Convert cheque_date list into space-separated string before saving
        if 'cheque_date' in validated_data:
            validated_data['cheque_date'] = " ".join(validated_data['cheque_date'])
        return super().create(validated_data)
    def update(self, instance, validated_data):
        # Same for update
        if 'cheque_date' in validated_data:
            validated_data['cheque_date'] = " ".join(validated_data['cheque_date'])
        return super().update(instance, validated_data)
   
    def to_representation(self, instance):
        rep = super().to_representation(instance)
 
        cheque_str = getattr(instance, 'cheque_date', '')
        if isinstance(cheque_str, str):
            rep['cheque_date'] = [
                date.strip() for date in cheque_str.strip().split(" ") if date.strip()
            ]
 
        return rep
    # def validate_submitted_by_agent(self, value):
    #     if not value:
    #         raise serializers.ValidationError("Agent is required.")
    #     return value
 
    class Meta:
        model = RentalProperties
        fields = '__all__'
        extra_kwargs = {
            'pms_contract': {'required': False},
            'owner_passport_copy': {'required': False},
            'owner_eid_copy': {'required': False},
            'pms_cheque_copy': {'required': False},
            'title_deed': {'required': False},
            'poa_pp': {'required': False},
            'poa_copy': {'required': False},
            'key_hand_over_form': {'required': False},
            'kyc_form': {'required': False},
            'form_status': {'required': False},
            'created_at': {'required': False},
            'updated_at': {'required': False},
            'created_by': {'required': False},
            'updated_by': {'required': False},
            'account': {'required': False},
            'status': {'required': False},
            'deal_sno': {'required': False},
            'approved_rejected_by': {'required': False},
            'comments_finance': {'required': False},
            'submitted_by_user_id': {'required': False},
            'agent_comment': {'required': False},
            'is_property_aml': {'required': False},
            'screening': {'required': False},
            'screening_comments': {'required': False},
            'seller_nationality': {'required': False},
            'buyer_nationality': {'required': False},
            'submitted_date': {'required': False},
            'manager_approved_rejected': {'required': False},
        }
 
 
    def create(self, validated_data):
        account_id = validated_data.pop('account_id', None)
        if account_id:
            validated_data['account_id'] = account_id
        return super().create(validated_data)
 
    def update(self, instance, validated_data):
        account_id = validated_data.pop('account_id', None)
        if account_id:
            validated_data['account_id'] = account_id
        return super().update(instance, validated_data)
   
 
    def validate_date_format(self, value, field_name):
        """
        Validate one or more space-separated dates in dd-mm-yyyy format.
        """
        if value:
            date_list = value.strip().split()
            for date_str in date_list:
                try:
                    datetime.strptime(date_str, '%d-%m-%Y')
                except ValueError:
                    raise serializers.ValidationError({
                        field_name: f"Invalid date format: '{date_str}'. Expected dd-mm-yyyy."
                    })
        return value
 
 
 
    def validate(self, data):
        # Validate date fields
        date_fields = [
            'deal_date', 'pm_start_date', 'pm_end_date',
            'tenancy_start_date', 'tenancy_end_date'
        ]
        for field in date_fields:
            value = data.get(field)
            if value:
                self.validate_date_format(value, field)
 
        # Validate cheque_date list
        # cheque_dates = data.get('cheque_date', [])
        # for i, date in enumerate(cheque_dates):
        #     if date:
        #         self.validate_date_format(date, f'cheque_date[{i}]')
 
        cheque_str = data.get('cheque_date', '')
        if cheque_str:
            for date_part in cheque_str.split():
                self.validate_date_format(date_part, 'cheque_date')
 
 
        # Validate required file fields
        # required_file_fields = [
        #     'pms_contract', 'owner_passport_copy', 'pms_cheque_copy',
        #     'title_deed', 'kyc_form', 'screening'
        # ]
        # for field in required_file_fields:
        #     existing_value = getattr(self.instance, field, "") if self.instance else ""
        #     new_value = data.get(field, existing_value)
        #     if not new_value:
        #         raise serializers.ValidationError({field: f"{field} is required."})
        # File validation
        if self.draft:
            # Only 'screening' is mandatory for draft
            if not data.get('screening') and not (self.instance and getattr(self.instance, 'screening', '')):
                raise serializers.ValidationError({'screening': "screening is required for draft."})
        else:
            # Full submission: all required files
            required_file_fields = [
                'pms_contract', 'owner_passport_copy', 'pms_cheque_copy',
                'title_deed', 'kyc_form', 'screening'
            ]
            for field in required_file_fields:
                existing_value = getattr(self.instance, field, "") if self.instance else ""
                new_value = data.get(field, existing_value)
                if not new_value:
                    raise serializers.ValidationError({field: f"{field} is required."})
        # Skip no_of_cheque validation when it's a draft
        if not self.draft:
            no_of_cheque = data.get('no_of_cheque')
            if no_of_cheque in [None, '']:
                raise serializers.ValidationError({'no_of_cheque': "This field is required in full submission."})
           
        # Conditionally require receipt_no only in full submission
        if not self.draft:
            receipt_no = data.get('receipt_no')
            if not receipt_no:
                raise serializers.ValidationError({'receipt_no': "This field is required in full submission."})
 
 
        # Ensure end dates are after start dates
        if data.get('pm_start_date') and data.get('pm_end_date'):
            pm_start = datetime.strptime(data['pm_start_date'], '%d-%m-%Y')
            pm_end = datetime.strptime(data['pm_end_date'], '%d-%m-%Y')
            if pm_end < pm_start:
                raise serializers.ValidationError({"pm_end_date": "PM End Date must be after PM Start Date."})
 
        if data.get('tenancy_start_date') and data.get('tenancy_end_date'):
            tenancy_start = datetime.strptime(data['tenancy_start_date'], '%d-%m-%Y')
            tenancy_end = datetime.strptime(data['tenancy_end_date'], '%d-%m-%Y')
            if tenancy_end < tenancy_start:
                raise serializers.ValidationError({"tenancy_end_date": "Tenancy End Date must be after Tenancy Start Date."})
 
        return data



User = get_user_model()
class AgentDropdownSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ['id', 'name']

    def get_name(self, obj):
        return f"{obj.name}".strip()
    




class ManagementReceiptsFilterSerializer(serializers.Serializer):
    """
    Serializer for filtering Rental Deals.
    """

    start = serializers.IntegerField(required=False, default=0)
    length = serializers.IntegerField(required=False, default=10)
    draw = serializers.IntegerField(required=False, default=0)
    type = serializers.CharField(required=False, allow_blank=True)

    search = SearchSerializer(required=False, default=dict)
    
    type = serializers.CharField(required=False, allow_blank=True)
    receipt_number = serializers.IntegerField(required=False)
    payment_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    status = serializers.CharField(required=False)
    agent_name = serializers.CharField(required=False)
    building_name = serializers.CharField(required=False)
    unit_number = serializers.CharField(required=False)
        
    date = serializers.DateField(
        required=False,
        input_formats=["%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"],
        allow_null=True
    )
    sec_date = serializers.DateField(
        required=False,
        input_formats=["%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"],
        allow_null=True
    )


    
class ManagementReceiptsSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d-%m-%Y")
    sec_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    deal_refer_no = serializers.CharField(required=False,allow_blank=True, allow_null=True)
    class Meta:
        model = ManagementReceipts
        fields = '__all__'  # includes all 22 fields in the model
    
