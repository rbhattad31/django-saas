from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Users

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import RentalDeals,Users
from .serializers import DealSerializer,filterSerializer
from .pagination import CustomPagination  
from rest_framework.pagination import PageNumberPagination  
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .forms import LoginForm, SignUpForm  # Add this import for LoginForm and SignUpForm
   

from django_filters import rest_framework as filters
from django.template import loader
from django import template
from django.urls import reverse


from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

class Rental_DealViewSet(viewsets.ModelViewSet):
    queryset = RentalDeals.objects.all()
       # for default `list`, `retrieve`
    pagination_class = CustomPagination 
    
    def get_serializer_class(self):
        if self.action == 'datatable_filter':
            return filterSerializer
        return DealSerializer # Custom pagination class

    @action(detail=False, methods=['post'] ,url_path='filter')
    def datatable_filter(self, request):
        print(request)

        serializer =  filterSerializer()
        print(request.user)
         
        user = Users.objects.get(email = request.user)
        print(user)

        
        print("Request data:", request.data)
        data = filterSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        data = data.validated_data
        print("validated", data)


        user = request.user

       
        # Superusers see everything
        if user.is_superuser:
            queryset = RentalDeals.objects.all()
         

        elif user.groups.filter(name="Manager").exists():
            # Managers see all approved and rejected deals
            queryset = RentalDeals.objects.filter(is_approved_rejected ="A")

        elif user.groups.filter(name="Finance").exists():
            # Finance sees only deals entered into the system
            queryset = RentalDeals.objects.filter(is_entered_finance_system="1")
 
      
        else:
            queryset = RentalDeals.objects.filter(submitted_by_user = user.id )

        print(queryset)






        # Global search
        search_term = data.get("search", {}).get("value") or ''
        print(search_term , "point x1")
     
        if search_term:
            print("point x2", queryset)
            queryset = queryset.filter(
                Q(submitted_by_user__name__icontains=search_term) |
                Q(reference_number__icontains=search_term) |
                Q(unit_details__icontains=search_term) |
                Q(building_name__icontains=search_term) |
                Q(project_name__icontains=search_term) |
                Q(owner_first_name__icontains=search_term) |
                Q(owner_last_name__icontains=search_term) |
                Q(owner_mobile__icontains=search_term) |
                Q(owner_email__icontains=search_term) |
                Q(tenant_first_name__icontains=search_term) |
                Q(tenant_last_name__icontains=search_term) |
                Q(tenant_mobile__icontains=search_term) |
                Q(tenant_email__icontains=search_term) |
                Q(property_usage__icontains=search_term) |
                Q(property_type__icontains=search_term) |
                Q(property_size__icontains=search_term) |
                Q(rental_price__icontains=search_term) |
                Q(security_deposit__icontains=search_term) |
                Q(mode_of_payment__icontains=search_term) |
                Q(premises_no__icontains=search_term) |
                Q(plot_no__icontains=search_term) |
                Q(created_at__icontains=search_term) |
                Q(updated_at__icontains=search_term)
            )
            print("pointx3",queryset )
           

        # Field-specific filters
        filter_fields = [
            "reference_number", "unit_details", "building_name", "deal_type",
            "deal_status", "project_name", "owner_name", "tenant_name",
            "owner_mobile", "tenant_mobile"
        ]
        for field in filter_fields:
            value = data.get(field)
            if value:
                filter_kwargs = {f"{field}__icontains": value}
                queryset = queryset.filter(**filter_kwargs)

        # Filterationon types keyword
        deal_type = data.get("type")
         
        if deal_type == "All":
            queryset = queryset.filter(form_status="Complete")
        

        elif deal_type == "draft":
            queryset = queryset.filter(form_status="Incomplete")
            

        elif deal_type == "approved":
            queryset = queryset.filter(is_approved_rejected="A" )

        elif deal_type == "rejected":
            queryset = queryset.filter(is_approved_rejected="R" )

        elif deal_type == "waiting":
            queryset = queryset.filter( is_approved_rejected="F")

        elif deal_type == "pending":
            queryset = queryset.filter(is_approved_rejected="P")

        elif deal_type == "pending-finance":
            queryset = queryset.filter(is_entered_in_finance_system="0")  
 
        elif deal_type == "entered-finance":
            queryset = queryset.filter(is_entered_in_finance_system="1")  
        else:
            return Response({"error": "Invalid deal type"}, status=400)
 

 
        print(queryset)

         
       


        # Date range filter
        if data.get("from"):
            queryset = queryset.filter(date__gte=data.get("from"))
        if data.get("to"):
            queryset = queryset.filter(date__lte=data.get("to"))

        # Pagination
        start = int(data.get("start") )  # Default to 0 if not provided
        length = int(data.get("length")) 
        print(start , length) # Default to 10 if not provided
        paginated = queryset[start:start + length]
        print("paginated", paginated)
        

        data = request.data.copy()  # Copy the original data to include in the responseda
        data.pop('csrfmiddlewaretoken', None)

        serializer =  DealSerializer(paginated, many=True,context={'request': request})
        response_data = {
            "draw": data.get("draw") ,  # Ensure draw is an integer
            "recordsTotal": queryset.count(),
            "recordsFiltered": queryset.count(),
            "data": serializer.data,
            # "input": data   
              # original input back
        } 

        return Response(response_data)


    @action(detail=False, methods=['post'], url_path='create-deal')
    def create_deal(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get','put'], url_path='update')
    def update_deal(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], url_path='delete-deal')
    def delete_deal(self, request, pk=None):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



Rental_DealViewSet_filter = Rental_DealViewSet.as_view({
    'post': 'datatable_filter'
})
Rental_DealViewSet_detail = Rental_DealViewSet.as_view({'get': 'retrieve'})
Rental_DealViewSet_filter = Rental_DealViewSet.as_view({'post': 'datatable_filter'})
Rental_DealViewSet_create = Rental_DealViewSet.as_view({'post': 'create_deal'})
Rental_DealViewSet_update = Rental_DealViewSet.as_view({'put': 'update', 'get': 'update'})
Rental_DealViewSet_delete = Rental_DealViewSet.as_view({'delete': 'delete_deal'})
 




def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            print(f'{username , password}')
            # user = Users.objects.get(email=username)
            # print()
            # print(user.check_password(password))
            
            user =  authenticate(email = username , password = password)
            print(user)
            
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})









@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def all_rental_deals(request):
    """
    View to list all rental deals.
    """
    return render(request, 'home/rentalall.html')