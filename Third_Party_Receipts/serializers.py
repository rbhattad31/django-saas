from rest_framework import serializers
from core.models import Deposits
from django.utils.html import format_html

class DepositsSerializer(serializers.ModelSerializer):
    action = serializers.SerializerMethodField()
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
            'unit_number','action'
        ]

    def get_DT_RowId(self, obj):
        return f"row_{obj.pk}"
    
    def get_action(self, obj):
        request = self.context.get('request')
     
        user = request.user
        html = ""

        # View
        if user.has_perm('core.view_deposits'):
            print("it has view permission ifromteh  serlozer")
            html += f' <a  style = "text-decoration: none;" href="/third_party_receipts/third-party/update/${obj.id}/" title="Edit" class="text-warning mx-1" style="font-size: 16px;"><i class="fas fa-edit"></i> </a>'

        # Edit (disallowed if approved unless special permission exists)
        if user.has_perm('core.change_deposits'):
            html += f'<a style = "text-decoration: none;" href="/third_party_receipts/third-party/view/${obj.id}/" title="View" class="text-primary mx-1" style="font-size: 16px;"><i class="fas fa-eye"></i></a>'
        else:
            html += ""

        # Delete
        if user.has_perm('core.delete_deposits'):
            html += f'<a style = "text-decoration: none;"  href="/third_party_receipts/recipts/download/${obj.id}/" title="Download" class="text-success mx-1" style="font-size: 16px;"> <i class="fas fa-download"></i> </a>'
        

        return format_html(html)



class DepositsfilterSerializer(serializers.Serializer):
    draw = serializers.IntegerField(required=False)
    start = serializers.IntegerField(required=False, default=0)
    length = serializers.IntegerField(required=False, default=10)

    search = serializers.DictField(required=False)

    
    from_date = serializers.DateField(required=False)
    to_date = serializers.DateField(required=False)

 