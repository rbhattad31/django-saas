from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import RentalDeals,Users
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
    serializer_class = filterSerializer  # for default `list`, `retrieve`
    pagination_class = CustomPagination  # Custom pagination class

    @action(detail=False, methods=['post'] ,url_path='filter')
    def datatable_filter(self, request):
        print("Request data:", request.data)
        data = filterSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        data = data.validated_data
        print("validated", data)
        
        queryset = RentalDeals.objects.all()






        # Global search
        search_term = data.get("search", {}).get("value") or ''
        if search_term:
            queryset = queryset.filter(
                Q(reference_number__icontains=search_term) |
                Q(building_name__icontains=search_term) |
                Q(unit_details__icontains=search_term) |
                Q(project_name__icontains=search_term) |
                Q(owner_name__icontains=search_term) |
                Q(tenant_name__icontains=search_term)
            )
            print("pointx1", queryset)

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

        elif deal_type == "waiting-finance":
            queryset = queryset.filter(is_entered_in_finance_system="0")  
 
        elif deal_type == "entered-finance":
            queryset = queryset.filter(is_entered_in_finance_system="1")  
        else:
            return Response({"error": "Invalid deal type"}, status=400)
 

 


         
       


        # Date range filter
        if data.get("from"):
            queryset = queryset.filter(date__gte=data.get("from"))
        if data.get("to"):
            queryset = queryset.filter(date__lte=data.get("to"))

        # Pagination
        start = int(data.get("start") )  # Default to 0 if not provided
        length = int(data.get("length"))  # Default to 10 if not provided
        paginated = queryset[start:start + length]
        print("paginated", paginated)
        

        data = request.data.copy()  # Copy the original data to include in the responseda
        data.pop('csrfmiddlewaretoken', None)

        serializer =  DealSerializer(paginated, many=True)
        response_data = {
            "draw": int(data.get("draw") or 0),  # Ensure draw is an integer
            "recordsTotal": queryset.count(),
            "recordsFiltered": queryset.count(),
            "data": serializer.data,
            "input": data    # original input back
        }

        return Response(response_data)




Rental_DealViewSet_filter = Rental_DealViewSet.as_view({
    'post': 'datatable_filter'
})
 




def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
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









# @login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


# @login_required(login_url="/login/")
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



# @login_required(login_url="/login/")
def all_rental_deals(request):
    """
    View to list all rental deals.
    """
    return render(request, 'home/rentalall.html')