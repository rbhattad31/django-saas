from rest_framework import serializers
from .models import RentalDeals

class DealSerializer(serializers.ModelSerializer):
    # agent_username = serializers.CharField(source='', read_only=True)
    class Meta:
        model = RentalDeals
        fields = '__all__'
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
    from_date = serializers.DateField(required=False, source="from", input_formats=["%Y-%m-%d"], allow_null=True)
    to_date = serializers.DateField(required=False, source="to", input_formats=["%Y-%m-%d"], allow_null=True)

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

    
     
             
        
