from rest_framework import serializers
from .models import Rental_Deal

class DealSerializer(serializers.ModelSerializer):
    agent_username = serializers.CharField(source='agent.username', read_only=True)
    class Meta:
        model = Rental_Deal
        fields = '__all__'
        extra_fields = ['agent_username']


    def validate(self, data):
        """
        Enforce required fields only when status is 'submitted'.
        """
        status = data.get('status', self.instance.status if self.instance else 'draft')

        if status == 'submitted':
            required_fields = [
                'agent',
                'deal_date',
                'reference_number',
                'deal_type',
                'project_name',
                'unit_number',
                'building_name',
                'deal_start_date',
                'deal_end_date',
            ]

            missing = [field for field in required_fields if not data.get(field)]
            if missing:
                raise serializers.ValidationError({
                    field: "This field is required when submitting." for field in missing
                })

        return data  
