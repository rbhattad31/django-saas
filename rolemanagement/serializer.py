from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from django.utils.html import format_html

class GroupSerializer(serializers.ModelSerializer):
    action  = serializers.SerializerMethodField()
    is_active  =  serializers.SerializerMethodField()
    account =  serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()



    permissions = serializers.SlugRelatedField(
        many=True,
        queryset=Permission.objects.all(),
        slug_field="codename"
    )
     
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions','action' , "is_active" , 'account',"description"]



    def get_is_active(self, obj):
        # Access GroupProfile.is_active safely
        if hasattr(obj, "profile"):
            return  "Active" if obj.profile.is_active else "Inactive"
        return None
    def get_description(self, obj):
        # Access GroupProfile.is_active safely
        if hasattr(obj, "profile"):
            return  obj.profile.description
        return None 
    def get_account(self, obj):
        # Access GroupProfile.is_active safely
        if hasattr(obj, "profile") and obj.profile.account:
            return {
                "id": obj.profile.account.id,
                "name": str(obj.profile.account.account_name)  # adjust field name
            }
        return None 



  

    def get_action(self, obj):
            request = self.context.get('request')
        
            user = request.user
            html = ""

            # View
            if user.has_perm('core.view_salesdeals'):
                print("it has view permission ifromteh  serlozer")
                html += f'<a href="/sales-deals/view/{obj.id}/" class="text-primary mr-2"><i class="fas fa-eye"></i></a>'

            # Edit (disallowed if approved unless special permission exists)

             
            print("it has view permission ifromteh  serlozer")
            html += f'<a href="/role/edit/{obj.id}/" class="text-primary mr-2"><i class="fas fa-edit"></i></a>'
        

            

            # Delete
            if user.has_perm('core.delete_salesdeals'):
                html += f'<a href="#" class="text-danger delete-btn" data-id="{obj.id}" data-bs-toggle="modal" data-bs-target="#deleteModal"><i class="fas fa-trash"></i></a>'

            return format_html(html)
    


class Groupfilter(serializers.Serializer):
     
    start = serializers.IntegerField(required=False, default=0)
    length = serializers.IntegerField(required=False, default=10)
    draw = serializers.IntegerField(required=False, default=0)

    search = serializers.DictField(required=False, default=dict)
    
 
     
     

