from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
import json
from core.models import SalesDeals
from core.models import Users 
from rest_framework.decorators import action
from .serializers import SalesDealSerializer , filterSerializer, AgentDropdownSerializer
from django.db.models import Q
from django.template import loader
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# from .forms import SalesDealsForm 
from django.template import TemplateDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings


# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets, status ,permissions

from .serializers import filterSerializer
# from .pagination import CustomPagination  
# from rest_framework.pagination import PageNumberPagination  
from .forms import LoginForm, SignUpForm  # Add this import for LoginForm and SignUpForm
   

from django.template import loader
from django import template
from django.urls import reverse



from django.db.models import Q


class SalesDealViewSet(viewsets.ModelViewSet):
    queryset = SalesDeals.objects.all()
    serializer_class = SalesDealSerializer

    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_sales(self, request, pk=None):
        sales = get_object_or_404(SalesDeals, pk=pk)
        sales.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=['get'], url_path='view')
    def view_sales_deal(self, request, pk=None):
        sales_deal = get_object_or_404(SalesDeals, pk=pk)
        serializer = SalesDealSerializer(sales_deal)
        # return HttpResponse("hello this is view page")
        aws_url = settings.AWS_URL


        return render(request, 'home/viewsalesdeal.html', {'salesdeal': serializer.data,'aws_base_url': aws_url})
    
    @action(detail=False, methods=['get','post'], url_path='update')
    def update_sales_deal(self, request,pk=None):
        pk = pk
        sales_deal = get_object_or_404(SalesDeals, pk=pk)
        serializer = SalesDealSerializer(sales_deal,   partial=True)
        
        return render(request, 'home/editsalesdeal.html', {'salesdeal': serializer.data})
    

               # if serializer.is_valid():
        #     serializer.save()
            # return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=False, methods=['post'], url_path='all')
    # def create_sales_deal(self, request, pk=None):
    #     pk=pk
    #     sales_deal=get_object_or_404(SalesDeals, pk=pk)
    #     serializer = SalesDealSerializer(sales_deal, partial=True)
    #     return render(request, 'home/createsalesdeal.html', {'salesdeal': serializer.data})
    
    @action(detail=False, methods=['post'], url_path='filter')
    def datatable_filter(self, request):
        data = filterSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        validated = data.validated_data
        print("Validated Data:", validated) 

        queryset = SalesDeals.objects.all()
        print("Initial Queryset:", queryset)  # Debugging line

        # Global search
        search_term = validated.get("search", {}).get("value") or ''
        if search_term:
            queryset = queryset.filter(
                # Q(email__icontains=search_term) |
                Q(reference_number__icontains=search_term) |
                Q(date__icontains=search_term) |
                Q(unit_details__icontains=search_term) |
                Q(builduing_name__icontains=search_term) |
                Q(project_name__icontains=search_term) |
                Q(unit_details__icontains=search_term) |

                Q(deal_amount__icontains=search_term) |
                Q(submitted_date__icontains=search_term)
            )
            print("Search Term:", search_term)  # Debugging line
        print("Filtered Queryset:", queryset)  # Debugging line
        # Field-specific filters
        filter_fields = [
            "reference_number", "unit_details", "building_name","seller_source","selller_mobile"
            "deal_status", "project_name","seller_name","buyer_name","buyer_mobile","buyer_source",
           ]
        for field in filter_fields:
            value = validated.get(field)
            if value:
                filter_kwargs = {f"{field}__icontains": value}
                queryset = queryset.filter(**filter_kwargs)

        # Deal Type Filter
        type = validated.get("type")
        if type == "All":
            queryset = queryset.filter(form_status="Complete")
        elif type == "draft":
            queryset = queryset.filter(form_status="Incomplete")
        elif type == "approved":
            queryset = queryset.filter(is_approved_rejected="A")
        elif type == "rejected":
            queryset = queryset.filter(is_approved_rejected="R")
        elif type == "waiting-for-finance":
            queryset = queryset.filter(is_approved_rejected="F")
        elif type == "pending":
            queryset = queryset.filter(is_approved_rejected="P")
        elif type == "pending-finance":
            queryset = queryset.filter(is_entered_in_finance_system="0")
        elif type == "entered-finance":
            queryset = queryset.filter(is_entered_in_finance_system="1")

        # Date range filter
        if validated.get("from_date"):
            queryset = queryset.filter(date__gte=validated.get("from_date"))
        if validated.get("to_date"):
            queryset = queryset.filter(date__lte=validated.get("to_date"))

        # Manual Pagination for DataTables
        start = validated.get("start", 0)
        length = validated.get("length", 10)
        paginated = queryset[start:start + length]

        serializer = SalesDealSerializer(paginated, many=True)
        response_data = {
            "draw": validated.get("draw", 0),
            "recordsTotal": queryset.count(),
            "recordsFiltered": queryset.count(),
            "data": serializer.data,
        }
        return Response(response_data)


SalesDealViewSet_filter = SalesDealViewSet.as_view({
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
def all_sales_deals(request):
    """
    View to list all rental deals.
    """
    return render(request, 'home/Salesall.html')


 # Ensure this form exists

# @login_required

from django.http import JsonResponse
from django.urls import reverse

from django.utils import timezone

@login_required(login_url="/login/")

def create_sales_deal_page(request):
    sales_data = {}
    agents=Users.objects.filter(is_active=True)
    agents=AgentDropdownSerializer(agents,many=True).data
    sales_data={
               'agents': agents,
           }
    print("Agents Data:", agents)
    if request.method == 'POST':
        print(request.POST)
        form = SalesDealsForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            print("Form is valid")
            sales_deal = form.save(commit=False)

            form_status = request.POST.get("form_status", "Complete")
            print("Form Status:", form_status)
            sales_deal.form_status = form_status

            
            

            # ✅ Set values not in the form
            sales_deal.submitted_by_user = request.user
            sales_deal.created_by = request.user.username
            sales_deal.is_deleted = '0'
            sales_deal.is_approved_rejected = 'N'
            sales_deal.is_entered_in_finance_system = 'N'
            sales_deal.date = timezone.now()

            sales_deal.save()
            for agent in agents:
                # You can process each agent here if needed
                pass

            if form_status == "Incomplete":
                return redirect('Sales-deal-draft')
            else:
                return redirect('Sales-deal')
    else:
        form = SalesDealsForm(user=request.user)

    return render(request, 'home/createsalesdeal.html', {'form': form,'sales_data' : json.dumps(sales_data)})
