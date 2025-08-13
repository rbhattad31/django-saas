from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status ,permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .serliaizer import UserSerializer , UsersfilterSerilizer
from core.models import Users 
from django.db.models import Q

# Create your views here.



class Userviewset(viewsets.ModelViewSet):
  queryset = Users.objects.all()
  @action(detail= True , methods= ["post"] , url_path = "filter")
  def datafilter_users(self,request):
    print("Request Data:", request.data)  # Debugging line
    data =  UsersfilterSerilizer(data=request.data)
    data.is_valid(raise_exception=True)
    validated = data.validated_data
    print("Validated Data:", validated) 

    queryset =  Users.objects.all()
    print("Initial Queryset:", queryset)  # Debugging line

    # Global search
    search_term = validated.get("search", {}).get("value") or ''
    if search_term:
        queryset = queryset.filter(
            Q(deposit_number__icontains=search_term) |
            Q(date__icontains=search_term) |
            Q(dhs__icontains=search_term) |
            Q(fils__icontains=search_term) |
            Q(payment_type__icontains=search_term) |
            Q(sec_date__icontains=search_term) |
            Q(deal_type__icontains=search_term) |
            Q(agent_name__icontains=search_term) |
            Q(project_name__icontains=search_term) |
            Q(building_name__icontains=search_term) |
            Q(unit_number__icontains=search_term)
        )

        print("Search Term:", search_term)  # Debugging line
    print("Filtered Queryset:", queryset)  # Debugging line
    # Field-specific filters
    filter_fields = [
                    'id', 'deposit_number', 'date', 'dhs', 'fils', 'payment_type',
                    'sec_date', 'deal_type', 'agent_name', 'project_name', 'building_name', 'unit_number'
                ]
    for field in filter_fields:
        value = validated.get(field)
        if value:
            filter_kwargs = {f"{field}__icontains": value}
            queryset = queryset.filter(**filter_kwargs)

    # Deal Type Filter
  

    # Date range filter
    if validated.get("from_date"):
        queryset = queryset.filter(date__gte=validated.get("from_date"))
    if validated.get("to_date"):
        queryset = queryset.filter(date__lte=validated.get("to_date"))

    # Manual Pagination for DataTables
    start = validated.get("start", 0)
    length = validated.get("length", 10)
    paginated = queryset[start:start + length]

    serializer =   UserSerializer(paginated, many=True , context = {'request': request})
    response_data = {
        "draw": validated.get("draw", 0),
        "recordsTotal": queryset.count(),
        "recordsFiltered": queryset.count(),
        "data": serializer.data,
    }
    return Response(response_data)









UserdatafilterViewset = Userviewset.as_view({"post": "datafilter_users"})

def filter(request):
    return render(request, "users_filter.html")





 