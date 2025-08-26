# Create your views here.
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models import Users, Account
from django.contrib.auth.models import Group
from accounts_management.serializers import UserSerializer,CreateUserSerializer,UpdateUserSerializer
from django.db.models import Q
from django_multitenant.utils import get_current_tenant
from django.shortcuts import get_object_or_404
from rest_framework import status

class UserListView(LoginRequiredMixin,PermissionRequiredMixin, APIView):
    permission_required = "core.view_user"  # <-- replace with your app_label.permission_codename
    raise_exception = True 
    def get(self, request):
        print("DEBUG: Entering UserListView.get()")
        roles = Group.objects.all()
        print("DEBUG: Fetched roles:", [role.name for role in roles])
        accounts = Account.objects.all()
        print("Users model fields:")
        for field in Users._meta.get_fields():
            print(field.name, field.get_internal_type())

        for field in Account._meta.get_fields():
           print("Account:",field.name, field.__class__.__name__)
        print("All account names:", [account.account_name for account in accounts])


        # print("All account names:", [account.name for account in accounts])
        # print("accounts:", [account.name for account in accounts])
        # print("DEBUG: Fetched accounts:", [account.name for account in accounts])
        users = Users.objects.all()
        print("DEBUG: Fetched all users in UserListView:", [{"id": user.id, "name": user.name, "email": user.email, "mobile_number": user.mobile_number } for user in users])
        site_url = request.build_absolute_uri('/')[:-1]  # remove trailing slash
        print("DEBUG: Site URL:", site_url)
        print("DEBUG: Rendering user_list.html with context")
        return render(request, 'home/user_list.html', {
            'roles': roles,
            'accounts': accounts,
            'users': users,
            'site_url': site_url,
        })

class UserDataListView(LoginRequiredMixin,PermissionRequiredMixin, APIView):
    permission_required = "core.view_user"  # <-- replace with your app_label.permission_codename
    raise_exception = True 
     


    def post(self, request):
        print("DEBUG: UserDataListView POST called")
        print("DEBUG: Entering UserDataListView.post()")
        print("DEBUG: Incoming POST data:", request.POST)
        # Pretty-print the incoming POST data
        for key, value in request.POST.items():
            print(f"{key}: {value}")

        # Optionally, print the columns mapping clearly
        print("\nDEBUG: DataTables columns mapping:")
        i = 0
        while f"columns[{i}][data]" in request.POST:
            col_data = request.POST.get(f"columns[{i}][data]")
            print(f"Column {i} → data key: '{col_data}'")
            i += 1
        
        draw = int(request.POST.get('draw', 1))
        print("DEBUG: Draw value:", draw)
        start = int(request.POST.get('start', 0))
        print("DEBUG: Start value:", start)
        length = int(request.POST.get('length', 10))
        print("DEBUG: Length value:", length)
        search_value = request.POST.get('search[value]', '')
        print("DEBUG: Search value:", search_value)
        role_filter = request.POST.get('role', '')
        print("DEBUG: Role filter:", role_filter)
        account_filter = request.POST.get('account', '')
        print("DEBUG: Account filter:", account_filter)

        # Sorting parameters
        order_column_idx = request.POST.get('order[0][column]', '1')
        order_dir = request.POST.get('order[0][dir]', 'asc')
        print(f"DEBUG: Sorting - Column index: {order_column_idx}, Direction: {order_dir}")

        # Map DataTable column index to model fields
        column_mapping = {
            '1': 'name',
            '2': 'email',
            '3': 'mobile_number',
            '4': 'is_active',  # Assuming status is mapped to is_active
            '5': 'created_at',  # Assuming created_date is created_at in the model
            '6': 'groups__name',  # Role name
            '7': 'account__account_name'  # Account name
        }
        order_field = column_mapping.get(order_column_idx, 'name')
        if order_dir == 'desc':
            order_field = f'-{order_field}'
        print(f"DEBUG: Ordering by field: {order_field}")

        # Get the current tenant
        current_tenant = get_current_tenant()
        print("DEBUG: Current tenant:", current_tenant)

        # Base queryset with tenant filtering
        queryset = Users.objects.all()
        print(f"DEBUG: Total records fetched: {queryset.count()}")
    
        # Print details of each user
        for user in queryset:
            user_data = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "mobile_number": user.mobile_number,

                # "status": getattr(user, "status", "None"),  # safe fallback
                # "created_date": user.created_date,
                # "role_name": user.groups.first().name if user.groups.exists() else "None",
                # "account_names": user.account.name if user.account else "None",
            }
            print("DEBUG: User data:", user_data)

        # print("DEBUG: Initial queryset (all users):", [{"id": user.id, "name": user.name, "email": user.email, "mobile_number": user.mobile_number, } for user in queryset])

        # if current_tenant:
        #     queryset = queryset.filter(account_id=current_tenant.id)

            # print("DEBUG: After tenant filter queryset (all users):", [{"id": user.id, "name": user.name, "email": user.email, "mobile_number": user.mobile_number, "status": user.status, "created_date": user.created_date, "role": user.groups.first().name if user.groups.exists() else "None", "account_name": user.account.name if user.account else "None"} for user in queryset])

        # Apply filters
        if role_filter:
            queryset = queryset.filter(groups__id=role_filter)
            #print("DEBUG: After role filter queryset (all users):", [{"id": user.id, "name": user.name, "email": user.email, "mobile_number": user.mobile_number, "status": user.status, "created_date": user.created_date, "role": user.groups.first().name if user.groups.exists() else "None", "account_name": user.account.name if user.account else "None"} for user in queryset])
        if account_filter:
            queryset = queryset.filter(account_id=account_filter)
            # print("DEBUG: After account filter queryset (all users):", [{"id": user.id, "name": user.name, "email": user.email, "mobile_number": user.mobile_number, "status": user.status, "created_date": user.created_date, "role": user.groups.first().name if user.groups.exists() else "None", "account_name": user.account.name if user.account else "None"} for user in queryset])
        # if search_value:
        #     queryset = queryset.filter(
        #         Q(name__icontains=search_value) |
        #         Q(email__icontains=search_value) |
        #         Q(mobile_number__icontains=search_value)
        #     )
            # print("DEBUG: After search filter queryset (all users):", [{"id": user.id, "name": user.name, "email": user.email, "mobile_number": user.mobile_number, "status": user.status, "created_date": user.created_date, "role": user.groups.first().name if user.groups.exists() else "None", "account_name": user.account.name if user.account else "None"} for user in queryset])

        if search_value:
            queryset = queryset.filter(
                Q(name__icontains=search_value) |
                Q(email__icontains=search_value) |
                Q(mobile_number__icontains=search_value) |
                Q(groups__name__icontains=search_value) |            # Role name
                Q(account__account_name__icontains=search_value) |  # Account name
                Q(created_at__icontains=search_value)               # Created date (string match)
            )

            # Handle status as special case (Active/Inactive)
            if search_value.lower() == 'active':
                queryset = queryset.filter(is_active=True)
            elif search_value.lower() == 'inactive':
                queryset = queryset.filter(is_active=False)


        # Total records before pagination
        total_records = queryset.count()
        print("DEBUG: Total records after filtering:", total_records)

        # Apply sorting
        queryset = queryset.order_by(order_field)

        # Apply pagination
        if length == -1:  # "All" option
            length = total_records
            print("DEBUG: Length set to 'All':", length)
        queryset = queryset[start:start + length]
        #print("DEBUG: Queryset after pagination (all users):", [{"id": user.id, "name": user.name, "email": user.email, "mobile_number": user.mobile_number, "status": user.status, "created_date": user.created_date, "role": user.groups.first().name if user.groups.exists() else "None", "account_name": user.account.name if user.account else "None"} for user in queryset])

        # Serialize data
        serializer = UserSerializer(queryset, many=True)
        data = serializer.data
        print("DEBUG: Serialized data:", data)
        print("\nDEBUG: Serialized user data:")
        for i, user in enumerate(data, 1):
            print(f"User {i}:")
            for key, value in user.items():
                print(f"  {key}: {value}")

        # Format response for DataTables
        response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': total_records,
            'data': data
        }
        print("DEBUG: Final response being sent:", response)

        return Response(response)
    
class UserCreateView(LoginRequiredMixin, APIView):
    def get(self, request):
        accounts = Account.objects.all()
        roles = Group.objects.all()
        # Hardcoded timezones; make a model if needed
        timezones = [
            {'value': 'Asia/Kolkata', 'text': 'Asia/Kolkata'},
            {'value': 'Asia/Dubai', 'text': 'Asia/Dubai'}
        ]
        return render(request, 'home/user_create.html', {
            'accounts': accounts,
            'roles': roles,
            'timezones': timezones
        })

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"success": True, "message": "User created successfully", "id": user.id})
        return Response({"success": False, "message": serializer.errors}, status=400)
    



class UserDetailView(LoginRequiredMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(Users, pk=pk)
        serializer = UserSerializer(user)
        accounts = Account.objects.all()
        roles = Group.objects.all()
        timezones = [
            {'value': 'Asia/Kolkata', 'text': 'Asia/Kolkata'},
            {'value': 'Asia/Dubai', 'text': 'Asia/Dubai'}
        ]
        image_url = user.image.url if user.image else None
        print(f"DEBUG: UserDetailView GET - image_url: {image_url}")

        print("DEBUG: UserDetailView GET - User timezone:", user.timezone)

        print("DEBUG: UserDetailView GET - User data:", serializer.data)
        return render(request, 'home/user_edit.html', {
            'user': serializer.data,
            'user_timezone': user.timezone,
            'accounts': accounts,
            'roles': roles,
            'timezones': timezones,
            'image_url': image_url,
        })

    def put(self, request, pk):
        user = get_object_or_404(Users, pk=pk)
        serializer = UpdateUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print("DEBUG: Updated user:", {"id": user.id, "timezone": user.timezone, "is_active": user.is_active})
            # print("DEBUG: Updated user is_active:", user.is_active)
            return Response({"success": True, "message": "User updated successfully"})
        return Response({"success": False, "message": serializer.errors}, status=400)

    def post(self, request, pk):
        user = get_object_or_404(Users, pk=pk)
        new_password = request.data.get('newPassword')
        confirm_password = request.data.get('confirmPassword')
        if new_password and new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            return Response({"success": True, "message": "Password updated successfully"})
        return Response({"success": False, "message": "Passwords do not match or are invalid"}, status=400)
    
class UserViewView(LoginRequiredMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            user = get_object_or_404(Users, pk=pk)
            serializer = UserSerializer(user)

            # Check for AJAX request
            # if request.headers.get("x-requested-with") == "XMLHttpRequest":
            #     return Response({"success": True, "data": serializer.data})
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                data = serializer.data.copy()  # copy serializer data
                # Add full image URL
                data['image_url'] = request.build_absolute_uri(user.image.url) if user.image else None
                return Response({"success": True, "data": data})

            # Normal page render
            accounts = Account.objects.all()
            roles = Group.objects.all()
            timezones = [
                {'value': 'Asia/Kolkata', 'text': 'Asia/Kolkata'},
                {'value': 'Asia/Dubai', 'text': 'Asia/Dubai'}
            ]

            
            return render(request, 'home/user_view.html', {
                'user': serializer.data,     # this feeds AJAX + readonly inputs
                'user_obj': user,            # real model object
                'user_timezone': getattr(user, "timezone", None),  # safe fetch
                'accounts': accounts,
                'roles': roles,
                'timezones': timezones
            })
        except Exception as e:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return Response({"success": False, "message": str(e)}, status=500)
            raise