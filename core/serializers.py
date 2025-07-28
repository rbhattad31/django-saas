from rest_framework import serializers
from core.models import RentalDeals,Users,Receipts
from rest_framework.reverse import reverse
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

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

    class Meta :
        model = Receipts
        fields = '__all__'

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

 


class SearchSerializer(serializers.Serializer):
    value = serializers.CharField(required=False, allow_blank=True)
    regex = serializers.BooleanField(required=False, default=False)


class DataTableSearchSerializer(serializers.Serializer):
    """
    Serializer for validating incoming DataTables AJAX request parameters,
    including custom search filters.
    """
    # --- Standard DataTables Parameters ---
    draw = serializers.IntegerField(required=True, min_value=0)
    start = serializers.IntegerField(required=True, min_value=0)
    length = serializers.IntegerField(required=True, min_value=1)

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
    from_date = serializers.CharField(source='from', required=False, allow_blank=True)
    to_date = serializers.CharField(source='to', required=False, allow_blank=True)
