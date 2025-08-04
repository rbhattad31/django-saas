from rest_framework import serializers
from core.models import SalesDeals,Users


class SalesDealSerializer(serializers.ModelSerializer):
    submitted_by = serializers.StringRelatedField(read_only=True)
    email = serializers.CharField( source="submitted_by_user.email" ,read_only=True)

    # Making the required fields optional and allow blank
    reference_number = serializers.CharField(required=False, allow_blank=True)
    unit_details = serializers.CharField(required=False, allow_blank=True)
    building_name = serializers.CharField(required=False, allow_blank=True)
    deal_status = serializers.CharField(required=False, allow_blank=True)
    project_name = serializers.CharField(required=False, allow_blank=True)
    screening_comments = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = SalesDeals
        fields = '__all__'


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