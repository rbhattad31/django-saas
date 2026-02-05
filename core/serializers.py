from rest_framework import serializers
from core.models import RentalDeals,Users,Receipts,SalesDeals
from rest_framework.reverse import reverse
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from django.utils.html import format_html

# class RentalDealSingleFieldSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RentalDeals
#         fields = ['is_entered_in_finance_system']


class ReceiptSerilizer(serializers.ModelSerializer):

    date = serializers.DateField(
        input_formats=["%d-%m-%Y"],   # Accept DMY from frontend
        format="%d-%m-%Y"             # Return DMY to frontend
    )
    sec_date = serializers.DateField(
        input_formats=["%d-%m-%Y"],   # Accept DMY from frontend
        format="%d-%m-%Y"             # Return DMY to frontend
    )
    # deal_end_date = serializers.DateField(
    #     input_formats=["%d-%m-%Y"],   # Accept DMY from frontend
    #     format="%d-%m-%Y"             # Return DMY to frontend
    # )
    reference_link = serializers.SerializerMethodField()

    class Meta :
        model = Receipts
        fields = '__all__'
        extra_fields = {
            'reference_link'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "data" in kwargs :
            print(kwargs)
            data = kwargs['data']
            payment_type = data.get('payment_type')

            if payment_type == 'Bank Transfer':
                # chequeNo is not required for Bank Transfer
                self.fields['cheque_no'].required = False
                # You might want to make bankName required
                self.fields['bank'].required = True

             

                

            elif payment_type == 'Cash':
                # Neither chequeNo nor bankName is required for Cash
                self.fields['cheque_no'].required = False
                self.fields['bank'].required = False

               

            elif payment_type == 'Cheque':
                # All fields are required for Cheque payment
                self.fields['cheque_no'].required = True
                self.fields['bank'].required = True


    def get_reference_link(self, obj):
        html=""
        # print(obj.deal_refer_no ,"thisiss the deal refer no")
        deal=None
        if obj.deal_refer_no:
            print(obj.deal_refer_no ,"thisiss the deal refer no entered if condition") 
            if obj.deal_type == "Rental":
                deal  = RentalDeals.objects.filter(reference_number=obj.deal_refer_no,is_deleted='N').first()
                if deal:
                    html += f'<a href="/rental-deals/view/{deal.id}/" target="_blank" style="text-decoration: none; color:black">{obj.deal_refer_no}</a>'
                else:
                    html +=""
            elif obj.deal_type == "Sales":
                deal  = SalesDeals.objects.filter(reference_number=obj.deal_refer_no,is_deleted="N").first()
                if deal:
                    html += f'<a href="/sales-deals/view/{deal.id}/" target="_blank" style="text-decoration: none;color:black ">{obj.deal_refer_no}</a>'
                else:
                    html +=""

        
 
            if deal: 
                return format_html(html) 
        else:
            return format_html(html)
            


 
         


class SearchSerializer(serializers.Serializer):
    value = serializers.CharField(required=False, allow_blank=True)
    regex = serializers.BooleanField(required=False, default=False)


class DataTableSearchSerializer(serializers.Serializer):
    """
    Serializer for validating incoming DataTables AJAX request parameters,
    including custom search filters.
    """
    # --- Standard DataTables Parameters ---
    draw = serializers.IntegerField(required=True,  )
    start = serializers.IntegerField(required=True,  )
    length = serializers.IntegerField(required=True,  )

    # The 'search' parameter is an object from DataTables
    search =  SearchSerializer(required=False)

    # --- Custom Filter Parameters from your frontend ---
    # type = serializers.CharField(required=False, allow_blank=True, default='All') # 'All' is default on frontend
    receipt_number = serializers.CharField(required=False, allow_blank=True, max_length=255)
    payment_type = serializers.CharField(required=False, allow_blank=True, max_length=255)
    deal_type = serializers.CharField(required=False, allow_blank=True, max_length=255)
    status = serializers.CharField(required=False, allow_blank=True, max_length=255)
    agent_name = serializers.CharField(required=False, allow_blank=True, max_length=255)
    unit_number = serializers.CharField(required=False, allow_blank=True, max_length=255)
    building_name = serializers.CharField(required=False, allow_blank=True, max_length=255)

    # --- Date Fields with Custom Validation for DD-MM-YYYY ---
    # These will be validated and converted to Python date objects
    # Note: The request sends 'from' and 'to', but we can't use those as field names (Python keywords)
    # So we declare the fields with different names and override to_internal_value
    from_field = serializers.DateField(required=False, allow_null=True, format='%d-%m-%Y', input_formats=['%d-%m-%Y', '%Y-%m-%d'])
    to_field = serializers.DateField(required=False, allow_null=True, format='%d-%m-%Y', input_formats=['%d-%m-%Y', '%Y-%m-%d'])
    
    def to_internal_value(self, data):
        # Map 'from' -> 'from_field' and 'to' -> 'to_field' before validation
        # Only map if the value is actually present (not empty string)
        data_copy = data.copy() if hasattr(data, 'copy') else dict(data)
        
        if 'from' in data_copy:
            from_value = data_copy.pop('from')
            # Only add to from_field if it has a non-empty value
            if from_value and from_value.strip():
                data_copy['from_field'] = from_value
                
        if 'to' in data_copy:
            to_value = data_copy.pop('to')
            # Only add to to_field if it has a non-empty value
            if to_value and to_value.strip():
                data_copy['to_field'] = to_value
        
        validated = super().to_internal_value(data_copy)
        
        # Map back to 'from' and 'to' in validated_data
        if 'from_field' in validated:
            validated['from'] = validated.pop('from_field')
        if 'to_field' in validated:
            validated['to'] = validated.pop('to_field')
        
        return validated