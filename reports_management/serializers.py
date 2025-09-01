from rest_framework import serializers
from core.models import RentalDeals, SalesDeals
from django.contrib.auth import get_user_model

User = get_user_model()
Users = get_user_model()
users = Users.objects.filter(is_active=True).order_by('name')

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User   # your custom Users model
        fields = ['id', 'full_name']

    def get_full_name(self, obj):
        # If you only have `name`, just return that
        return obj.name or obj.email  # fallback if name is empty
    
class AgentDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id", "name"]

   

class AgentCommissionSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='id')
    primary_agent = serializers.SerializerMethodField()
    secondary_agent = serializers.SerializerMethodField()
    deal_type = serializers.CharField()
    reference_number = serializers.CharField(source='reference_number')
    unit_details = serializers.CharField(source='unit_details', allow_null=True, allow_blank=True)
    project_name = serializers.CharField(source='project_name', allow_null=True, allow_blank=True)
    building_name = serializers.CharField(source='building_name', allow_null=True, allow_blank=True)
    price = serializers.SerializerMethodField()
    deal_date = serializers.DateField(source='date')
    gross_commission = serializers.CharField(source='total_commission', allow_null=True, allow_blank=True)
    net_commission = serializers.CharField(source='net_commission', allow_null=True, allow_blank=True)

    # def get_primary_agent(self, obj):
    #     return f"{obj.agent_name1 or ''} {obj.agent_name2 or ''}".strip() or 'Unknown'

    # def get_secondary_agent(self, obj):
    #     return f"{obj.agent_name2 or ''} {obj.agent_name3 or ''}".strip() or 'Unknown'

    def get_primary_agent(self, obj):
        primary = f"{obj.agent_name1 or ''} {obj.agent_name2 or ''}".strip() or 'Unknown'
        print("DEBUG: get_primary_agent -> agent_name1:", obj.agent_name1, "agent_name2:", obj.agent_name2, "=> Primary:", primary)
        return primary

    def get_secondary_agent(self, obj):
        secondary = f"{obj.agent_name2 or ''} {obj.agent_name3 or ''}".strip() or 'Unknown'
        print("DEBUG: get_secondary_agent -> agent_name2:", obj.agent_name2, "agent_name3:", obj.agent_name3, "=> Secondary:", secondary)
        return secondary


    def get_price(self, obj):
        if isinstance(obj, RentalDeals):
            return f"AED {obj.rental_price or '0.00'}/-"
        elif isinstance(obj, SalesDeals):
            return f"AED {obj.deal_amount or '0.00'}/-"
        return '0.00'


class RentalDealsSerializer(serializers.ModelSerializer):
    # primary_agent = serializers.SerializerMethodField()
    secondary_agent = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    deal_type = serializers.SerializerMethodField()  # <--- Add here
    deal_date = serializers.DateField(source='date')
    gross_commission = serializers.CharField(source='total_commission', allow_null=True, allow_blank=True)
    submitted_by_agent = serializers.IntegerField(
        source='submitted_by_user_id',
        required=False,
        allow_null=True
    )

    class Meta:
        model = RentalDeals
        fields = [
            'id', 'submitted_by_agent','primary_agent', 'secondary_agent', 'deal_type', 'reference_number',
            'unit_details', 'project_name', 'building_name', 'price', 'date',
            'total_commission', 'deal_date', 'gross_commission','net_commission'
        ]

    primary_agent = serializers.SerializerMethodField()

    
    # def get_primary_agent(self, obj):
    #     if obj.submitted_by_user_id:
    #         user = Users.objects.filter(id=obj.submitted_by_user_id).first()
    #         if user:
    #             resolved_user = user.name
    #         else:
    #             resolved_user = f"{obj.agent_name1 or 'Unknown'}"  # fallback to agent_name1
    #             print(f"[MISSING USER] obj.id={obj.id}, submitted_by_user_id={obj.submitted_by_user_id}, fallback_agent_name1={resolved_user}")
    #         print(f"[DEBUG] get_primary_agent -> obj.id={obj.id}, submitted_by_user_id={obj.submitted_by_user_id}, resolved_user={resolved_user}")
    #         return str(resolved_user)
    #     print(f"[DEBUG] get_primary_agent -> obj.id={obj.id}, submitted_by_user_id=None")
    #     return "Unknown"
    
    # def get_primary_agent(self, obj):
        
    #     if obj.submitted_by_user_id:
    #         user = Users.objects.filter(id=obj.submitted_by_user_id).first()
    #         if user:
    #             resolved_user = user.name
    #         else:
    #             resolved_user = "Unknown"
    #             print(f"[MISSING USER] obj.id={obj.id}, submitted_by_user_id={obj.submitted_by_user_id}")
    #         print(f"[DEBUG] get_primary_agent -> obj.id={obj.id}, resolved_user={resolved_user}")
    #         return str(resolved_user)
        
    #     print(f"[DEBUG] get_primary_agent -> obj.id={obj.id}, resolved_user=Unknown")
    #     return "Unknown"




    # def get_secondary_agent(self, obj):
    #     resolved_secondary = obj.agent_name1 or "Unknown"
    #     print(f"[DEBUG] get_secondary_agent -> obj.id={obj.id}, resolved_secondary={resolved_secondary}")
    #     return resolved_secondary

    # def get_primary_agent(self, obj):
    #     user = getattr(obj, 'submitted_by_user', None)
    #     resolved_user = user.name if user else "Unknown"
    #     print(f"[DEBUG] get_primary_agent -> obj.id={obj.id}, resolved_user={resolved_user}")
    #     return resolved_user


    # def get_secondary_agent(self, obj):
    #     resolved_secondary = obj.agent_name1 or "Unknown"
    #     print(f"[DEBUG] get_secondary_agent -> obj.id={obj.id}, resolved_secondary={resolved_secondary}")
    #     return resolved_secondary
    
    def get_primary_agent(self, obj):
        user = getattr(obj, 'submitted_by_user', None)
        resolved_user = str(user.name) if user and user.name else "Unknown"
        return resolved_user

    # def get_secondary_agent(self, obj):
    #     resolved_secondary = str(obj.agent_name1) if obj.agent_name1 else "Unknown"
    #     return resolved_secondary

    def get_secondary_agent(self, obj):
        agent_name = str(obj.agent_name1) if obj.agent_name1 else None
        user_map = self.context.get('user_map', {})
        if agent_name and agent_name.isdigit():
            return user_map.get(agent_name, "Unknown")
        return agent_name if agent_name else "Unknown"
    
  


    # def get_primary_agent(self, obj):
    #     return f"{obj.agent_name1 or ''} {obj.agent_name2 or ''}".strip() or 'Unknown'

    # def get_secondary_agent(self, obj):
    #     return f"{obj.agent_name2 or ''} {obj.agent_name3 or ''}".strip() or 'Unknown'

    

    def get_price(self, obj):
        return f"AED {obj.rental_price or '0.00'}/-"

    def get_deal_type(self, obj):
        return 'Rental'


class SalesDealsSerializer(serializers.ModelSerializer):
    primary_agent = serializers.SerializerMethodField()
    secondary_agent = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    deal_type = serializers.SerializerMethodField()  # <--- Add here
    building_name = serializers.CharField(source='builduing_name')  # map your model typo
    deal_date = serializers.DateField(source='date')
    gross_commission = serializers.CharField(source='total_commission', allow_null=True, allow_blank=True)

    class Meta:
        model = SalesDeals
        fields = [
            'id', 'primary_agent', 'secondary_agent', 'deal_type', 'reference_number',
            'unit_details', 'project_name', 'building_name', 'price', 'date',
            'total_commission', 'deal_date', 'gross_commission','net_commission'
        ]


    def get_primary_agent(self, obj):
        user = getattr(obj, 'submitted_by_user', None)
        resolved_user = str(user.name) if user and user.name else "Unknown"
        return resolved_user
    
    # def get_primary_agent(self, obj):
    #     return f"{obj.agent_name1 or ''} {obj.agent_name2 or ''}".strip() or 'Unknown'

    # def get_secondary_agent(self, obj):
    #     return f"{obj.agent_name2 or ''} {obj.agent_name3 or ''}".strip() or 'Unknown'
    # def get_secondary_agent(self, obj):
    #     resolved_secondary = str(obj.agent_name1) if obj.agent_name1 else "Unknown"
    #     return resolved_secondary
    def get_secondary_agent(self, obj):
        agent_name = str(obj.agent_name1) if obj.agent_name1 else None
        user_map = self.context.get('user_map', {})
        if agent_name and agent_name.isdigit():
            return user_map.get(agent_name, "Unknown")
        return agent_name if agent_name else "Unknown"

    def get_price(self, obj):
        return f"AED {obj.deal_amount or '0.00'}/-"

    def get_deal_type(self, obj):
        return 'Sales'




# from rest_framework import serializers
# from core.models import RentalDeals, SalesDeals
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class AgentDropdownSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "name"]

# class RentalDealsSerializer(serializers.ModelSerializer):
#     primary_agent = serializers.SerializerMethodField()
#     secondary_agent = serializers.SerializerMethodField()
#     price = serializers.SerializerMethodField()
#     deal_type = serializers.SerializerMethodField()
#     deal_date = serializers.DateField(source='date')
#     gross_commission = serializers.CharField(source='total_commission', allow_null=True, allow_blank=True)

#     class Meta:
#         model = RentalDeals
#         fields = [
#             'id', 'primary_agent', 'secondary_agent', 'deal_type', 'reference_number',
#             'unit_details', 'project_name', 'building_name', 'price', 'deal_date',
#             'gross_commission', 'net_commission'
#         ]

#     def get_primary_agent(self, obj):
#         user = getattr(obj, 'submitted_by_user', None)
#         return str(user.name) if user and user.name else "Unknown"

#     def get_secondary_agent(self, obj):
#         return str(obj.agent_name1) if obj.agent_name1 else "Unknown"

#     def get_price(self, obj):
#         return f"AED {obj.rental_price or '0.00'}/-"

#     def get_deal_type(self, obj):
#         return 'Rental'

# class SalesDealsSerializer(serializers.ModelSerializer):
#     primary_agent = serializers.SerializerMethodField()
#     secondary_agent = serializers.SerializerMethodField()
#     price = serializers.SerializerMethodField()
#     deal_type = serializers.SerializerMethodField()
#     building_name = serializers.CharField(source='building_name')
#     deal_date = serializers.DateField(source='date')
#     gross_commission = serializers.CharField(source='total_commission', allow_null=True, allow_blank=True)

#     class Meta:
#         model = SalesDeals
#         fields = [
#             'id', 'primary_agent', 'secondary_agent', 'deal_type', 'reference_number',
#             'unit_details', 'project_name', 'building_name', 'price', 'deal_date',
#             'gross_commission', 'net_commission'
#         ]

#     def get_primary_agent(self, obj):
#         return f"{obj.agent_name1 or ''} {obj.agent_name2 or ''}".strip() or 'Unknown'

#     def get_secondary_agent(self, obj):
#         return f"{obj.agent_name2 or ''} {obj.agent_name3 or ''}".strip() or 'Unknown'

#     def get_price(self, obj):
#         return f"AED {obj.deal_amount or '0.00'}/-"

#     def get_deal_type(self, obj):
#         return 'Sales'