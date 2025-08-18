from django.shortcuts import render

# Create your views here.


from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group, Permission
from core.models import GroupProfile,Account
from  .serializer import GroupSerializer
from django.db.models import Q

class RoleMangementViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        Return only roles (groups) that belong to the same account id.
        Group names are stored like '8-admin', '12-sales' etc.
        """
        account_id =  request.user.account_id
        if not account_id:
            return Response({"detail": "Account not found"}, status=400)

        prefix = f"{account_id}-"  # e.g. "8-"
        queryset = self.queryset.filter(name__startswith=prefix)

        # if you want to strip the "8-" part before returning
        roles = GroupSerializer(queryset, many=True , context = {"request" : request})

        return Response(roles.data)
    
    @action(detail=False, methods=['post'] ,url_path='filter')
    def datatable_filter(self, request):
        print(request.data)
        data = request.data
        print(request.data.get("order") ,"togetordering")
        user =  request.user
        print(request.user)
        account_id = user.account_id
        print( "account_from_request",request.user.account_id)

        account_id = user.account_id
        prefix = f"{account_id}-"
        queryset = Group.objects.filter(name__startswith=prefix)

       

         

        
        






        # Global search
        search_term = data.get("search", {}).get("value") or ''
        print(search_term , "point x1")
        combined_q_object = Q()
     
        combined_q_object |= Q(name__icontains=search_term)
       
   

        # --- Specific Handling for Date Fields ---
         
            # If your date fields are DATETIME/TIMESTAMP, you might need a range query
            # For example, to search for '2017-04-11' in a DATETIME field:
            # from datetime import timedelta
            # end_of_day = parsed_date + timedelta(days=1)
            # combined_q_object |= Q(date__range=(parsed_date, end_of_day))
            # combined_q_object |= Q(deal_start_date__range=(parsed_date, end_of_day))
            # combined_q_object |= Q(deal_end_date__range=(parsed_date, end_of_day))


       

        # Apply the combined Q object to the queryset

        print("point x2", queryset)
        queryset = queryset.filter(combined_q_object) 
         


         
       
     
          

         
       

 

        # Pagination
        start = int(data.get("start") )  # Default to 0 if not provided
        length = int(data.get("length")) 
        print(start , length) # Default to 10 if not provided
        paginated = queryset[start:start + length]
        print("paginated", paginated)
      
        

        data = request.data.copy()  # Copy the original data to include in the responseda
        data.pop('csrfmiddlewaretoken', None)

        # Define queryset for filtered roles/groups
       

        serializer = GroupSerializer(paginated ,  many=True, context={'request': request})
        response_data = {
            "draw": data.get("draw"),  # Ensure draw is an integer
            "recordsTotal": queryset.count(),
            "recordsFiltered": queryset.count(),
            "data": serializer.data,
            # "input": data   
              # original input back
        }

        return Response(response_data , status= status.HTTP_200_OK)
    

    def create(self,request):
        print(request.data)
        data = request.data
        role_name = data.get("role_name")
        description = data.get("description", "")
        permissions = data.get("permissions", [])



        group, created = Group.objects.get_or_create(name=role_name)



        # Optional: store description in separate model if needed
        # Example: RoleProfile with FK to Group

        # Clear old permissions first
        group.permissions.clear()

        # Attach selected permissions
        for perm_codename in permissions:
            try:
                perm = Permission.objects.get(codename=perm_codename)
                group.permissions.add(perm)
            except Permission.DoesNotExist:
                pass  # skip invalid permissions
        account = Account.objects.get(id=request.user.account_id)
        profile, _ = GroupProfile.objects.get_or_create(group=group)
        profile.account = account
       
        profile.description = description
        profile.save()

        return Response(  "Role Created successfully", status=status.HTTP_200_OK )
    


    @action(detail=True, methods=["get", "post"], url_path="update-role")
    def update_role(self, request, pk=None):
        """
        GET  -> Fetch role details (with permissions, profile info)
        POST -> Update role details (name, description, permissions, etc.)

        """

        print(pk)
        group = Group.objects.filter(id = pk).first()
        print(group)

        if request.method == "GET":
            serializer = GroupSerializer(group ,context = {"request":request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == "PUT":
            data = request.data

            # Update name
            if "name" in data:
                group.name = data["name"]
                group.save()

            # Update permissions
            if "permissions" in data:
                group.permissions.clear()
                for codename in data["permissions"]:
                    try:
                        perm = Permission.objects.get(codename=codename)
                        group.permissions.add(perm)
                    except Permission.DoesNotExist:
                        continue

            # Update GroupProfile
            profile, _ = GroupProfile.objects.get_or_create(group=group)
            if "description" in data:
                profile.description = data["description"]
            if "account" in data:
                profile.account_id = data["account"]
            if "status" in data:
                profile.status = data["status"]
            profile.save()

            serializer = GroupSerializer(group,context = {"request":request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        





Role_filter  =  RoleMangementViewSet.as_view({'post': 'datatable_filter'})

Role_list_view = RoleMangementViewSet.as_view({'post': 'list'})
Role_create_view = RoleMangementViewSet.as_view({'post': 'create'})
Role_retrieve_view = RoleMangementViewSet.as_view({'get': 'retrieve'})
Role_update_view = RoleMangementViewSet.as_view({'put': 'update_role' ,"get":"update_role"})
Role_partial_update_view = RoleMangementViewSet.as_view({'patch': 'partial_update'})
Role_delete_view = RoleMangementViewSet.as_view({'delete': 'destroy'})











def role_managementlist_html(request):
  return render(request , "rolelist.html")

def role_management_create(request):
    return render(request , "role_create.html")

def role_management_update(request,pk=None):
    return render(request , "role_edit.html" ,{"role_id":pk})

def role_management_view(request,pk=None):
    print(pk)
    group = Group.objects.filter(id = pk).first()
    print(group)

    

    if request.method == "GET":
        serializer = GroupSerializer(group ,context = {"request":request})

        return render(request , "role_view.html" ,{ "role_id":pk})

    
















