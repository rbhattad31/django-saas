from rest_framework import serializers
from core.models import Deposits

class DepositsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposits
        fields = [
            'id',  # <-- include this!
            'deposit_number',
            'date',
            'dhs',
            'fils',
            'payment_type',
            'sec_date',
            'deal_type',
            'agent_name',
            'project_name',
            'building_name',
            'unit_number'
        ]

    def get_DT_RowId(self, obj):
        return f"row_{obj.pk}"

class DepositsfilterSerializer(serializers.Serializer):
    draw = serializers.IntegerField(required=False)
    start = serializers.IntegerField(required=False, default=0)
    length = serializers.IntegerField(required=False, default=10)

    search = serializers.DictField(required=False)

    
    from_date = serializers.DateField(required=False)
    to_date = serializers.DateField(required=False)

 