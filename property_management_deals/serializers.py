 


from rest_framework import serializers
from core.models import RentalProperties,Users,ManagementReceipts
from django.contrib.auth import get_user_model

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
 
    def get_can_view(self, obj):
        # obj is the RentalDeal instance for the current row
        request = self.context.get('request')
        if not request:
            print("enter data ")
            return False # No request context, cannot determine permissions
 
        # Example: User must have 'change_rentaldeal' permission and deal must not be 'archived'
        # Replace 'your_app.change_rentaldeal' with your actual permission string
        has_permission = request.user.has_perm('core.view_properties_rentalproperties')
        # is_editable_status = obj.status != 'archived' # Example status check
 
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
    # print("Search item:",search)

    reference_no = serializers.CharField(required=False, allow_blank=True)
    building_name = serializers.CharField(required=False, allow_blank=True)
    unit_no = serializers.CharField(required=False, allow_blank=True)
    project_name = serializers.CharField(required=False, allow_blank=True)
    property_id = serializers.CharField(required=False, allow_blank=True)
    approval_status = serializers.CharField(required=False, allow_blank=True)

    deal_date_from = serializers.DateField(required=False, input_formats=["%Y-%m-%d"], allow_null=True)
    deal_date_to = serializers.DateField(required=False, input_formats=["%Y-%m-%d"], allow_null=True)
    pm_date_from = serializers.DateField(required=False, input_formats=["%Y-%m-%d"], allow_null=True)
    pm_date_to = serializers.DateField(required=False, input_formats=["%Y-%m-%d"], allow_null=True)
    tenancy_date_from = serializers.DateField(required=False, input_formats=["%Y-%m-%d"], allow_null=True)
    tenancy_date_to = serializers.DateField(required=False, input_formats=["%Y-%m-%d"], allow_null=True)




class PropertySerializer(serializers.ModelSerializer):
    is_deleted = serializers.ChoiceField(
        choices=[('Y', 'Yes'), ('N', 'No')],
        default='N',
        allow_blank=False
    )
    is_approved_rejected = serializers.ChoiceField(
        choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected'), ('W', 'Waiting Finance')],
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
    deal_date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'], required=False, allow_null=True)
    pm_start_date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'], required=False, allow_null=True)
    pm_end_date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'], required=False, allow_null=True)
    tenancy_start_date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'], required=False, allow_null=True)
    tenancy_end_date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'], required=False, allow_null=True)
    

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

        def validate(self, data):
            required_file_fields = [
                'pms_contract', 'owner_passport_copy', 'pms_cheque_copy',
                'title_deed', 'kyc_form', 'screening'
            ]
            for field in required_file_fields:
                # Check if field is in data or exists in instance (for updates)
                existing_value = getattr(self.instance, field, "") if self.instance else ""
                new_value = data.get(field, existing_value)
                if not new_value:
                    raise serializers.ValidationError({field: f"{field} is required."})
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
    #print("Search item:",search)
    
    

    type = serializers.CharField(required=False, allow_blank=True)
    receipt_number = serializers.IntegerField(required=False)
    payment_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    status = serializers.CharField(required=False)
    agent_name = serializers.CharField(required=False)
    building_name = serializers.CharField(required=False)
    unit_number = serializers.CharField(required=False)

    
class ManagementReceiptsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagementReceipts
        fields = '__all__'  # includes all 22 fields in the model
    
