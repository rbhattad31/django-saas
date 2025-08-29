from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from core.models import SalesDeals,Users
from django.utils.html import format_html


class SalesDealSerializer(serializers.ModelSerializer):
 
    email = serializers.CharField( source="submitted_by_user.email" ,read_only=True)
    action = serializers.SerializerMethodField()

    # Making the required fields optional and allow blank
    reference_number = serializers.CharField(required=False, allow_blank=True, validators=[
            UniqueValidator(
                queryset=SalesDeals.objects.all(),
                message="This reference number already exists."
            )])
    unit_details = serializers.CharField(required=False, allow_blank=True)
    building_name = serializers.CharField(required=False, allow_blank=True)
    deal_status = serializers.CharField(required=False, allow_blank=True)
    project_name = serializers.CharField(required=False, allow_blank=True)
    screening_comments = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = SalesDeals
        fields = '__all__'

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


class filterSerializer(serializers.Serializer):
    draw = serializers.IntegerField(required=False)
    start = serializers.IntegerField(required=False, default=0)
    length = serializers.IntegerField(required=False, default=10)

    search = serializers.DictField(required=False)

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
    manager_cheque_copy = serializers.FileField(required=False, allow_null=True)
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