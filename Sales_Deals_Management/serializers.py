from rest_framework import serializers
from .models import SalesDeal

class SalesDealSerializer(serializers.ModelSerializer):
    submitted_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SalesDeal
        fields = '__all__'
       
# class SourceDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SourceDetails
#         fields = '__all__'