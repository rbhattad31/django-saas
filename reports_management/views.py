 






import logging
from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.contrib.auth import get_user_model
from core.models import RentalDeals, SalesDeals
from .serializers import RentalDealsSerializer, SalesDealsSerializer, AgentDropdownSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from collections import defaultdict
from rest_framework.decorators import api_view, permission_classes, action
import re



logger = logging.getLogger(__name__)

User = get_user_model()
Users = get_user_model()



def safe_float(value):
    """Extracts the first valid float from messy strings"""
    if isinstance(value, (int, float)):
        return float(value)
    if not value:
        return 0.0
    match = re.search(r'[-+]?\d*\.?\d+', str(value))
    return float(match.group()) if match else 0.0


def agent_commission_report(request):
    logger.debug("Rendering agent commission report page")
    return render(request, 'home/agent_commission_report.html')

def agent_performance_report(request):
    logger.debug("Rendering agent performance report page")
    return render(request, 'home/agent_performance_report.html')

class AgentCommissionReportViewSet(ViewSet):
    def datatable_filter(self, request):
        draw = int(request.POST.get('draw', 1))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 10))
        reference_number = request.POST.get('reference_number', '')
        unit_details = request.POST.get('unit_details', '')
        building_name = request.POST.get('building_name', '')
        project_name = request.POST.get('project_name', '')
        agent_name = request.POST.get('agent_name', '')
        deal_type = request.POST.get('deal_type', '')
        date_from = request.POST.get('from', '')
        date_to = request.POST.get('to', '')

        # Filter RentalDeals
        #rental_qs = RentalDeals.objects.filter(is_deleted='N')
        rental_qs = RentalDeals.objects.filter(is_deleted='N',account_id = request.user.account_id).prefetch_related('submitted_by_user')

        if reference_number:
            rental_qs = rental_qs.filter(reference_number__icontains=reference_number)
        if unit_details:
            rental_qs = rental_qs.filter(unit_details__icontains=unit_details)
        if building_name:
            rental_qs = rental_qs.filter(building_name__icontains=building_name)
        if project_name:
            rental_qs = rental_qs.filter(project_name__icontains=project_name)
        if agent_name:
            rental_qs = rental_qs.filter(
                Q(agent_name1__icontains=agent_name) |
                Q(agent_name2__icontains=agent_name) |
                Q(agent_name3__icontains=agent_name)
            )
        if deal_type == 'Sales':
            rental_qs = rental_qs.none()
        if date_from:
            rental_qs = rental_qs.filter(date__gte=date_from)
        if date_to:
            rental_qs = rental_qs.filter(date__lte=date_to)

        # DataTables search bar
        search_value = request.POST.get('search[value]', '').strip().lower()

        # Filter SalesDeals
        #sales_qs = SalesDeals.objects.filter(is_deleted='N')
        sales_qs = SalesDeals.objects.filter(is_deleted='N').prefetch_related('submitted_by_user')

        if reference_number:
            sales_qs = sales_qs.filter(reference_number__icontains=reference_number)
        if unit_details:
            sales_qs = sales_qs.filter(unit_details__icontains=unit_details)
        if building_name:
            sales_qs = sales_qs.filter(builduing_name__icontains=building_name)  # mapping typo
        if project_name:
            sales_qs = sales_qs.filter(project_name__icontains=project_name)
        if agent_name:
            sales_qs = sales_qs.filter(
                Q(agent_name1__icontains=agent_name) |
                Q(agent_name2__icontains=agent_name) |
                Q(agent_name3__icontains=agent_name)
            )
        if deal_type == 'Rental':
            sales_qs = sales_qs.none()
        if date_from:
            sales_qs = sales_qs.filter(date__gte=date_from)
        if date_to:
            sales_qs = sales_qs.filter(date__lte=date_to)

        # Serialize separately
        rental_data = RentalDealsSerializer(rental_qs, many=True).data
        sales_data = SalesDealsSerializer(sales_qs, many=True).data

        # Combine in Python
        combined_data = rental_data + sales_data

        # Global search across all columns
        if search_value:
            def matches_search(row):
                for key, value in row.items():
                    if value and search_value in str(value).lower():
                        return True
                return False
            combined_data = list(filter(matches_search, combined_data))

        # Sorting
        order_column_idx = int(request.POST.get('order[0][column]', 0))
        order_dir = request.POST.get('order[0][dir]', 'asc')
        order_columns = [
            'primary_agent', 'secondary_agent', 'deal_type', 'reference_number',
            'unit_details', 'project_name', 'building_name', 'price',
            'deal_date', 'gross_commission', 'net_commission'
        ]
        order_field = order_columns[order_column_idx]
        combined_data.sort(key=lambda x: x.get(order_field) or '', reverse=(order_dir=='desc'))

        # Pagination
        page_data = combined_data[start:start+length]

        return Response({
            'draw': draw,
            'recordsTotal': len(combined_data),
            'recordsFiltered': len(combined_data),
            'data': page_data
        }, status=status.HTTP_200_OK)

    def agent_dropdown(self, request):
        users = Users.objects.filter(is_active=True).order_by("name")
        serializer = AgentDropdownSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # @csrf_exempt
    # @api_view(['POST'])
    # @permission_classes([])
    @action(detail=False, methods=['post'], url_path='performance-datatable')
    def performance_datatable_filter(self, request):
        draw = int(request.POST.get('draw', 1))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 10))
        agent_name = request.POST.get('agent_name', '')
        deal_type = request.POST.get('deal_type', '')
        minimum_deals = request.POST.get('minimum_deals', '')
        maximum_deals = request.POST.get('maximum_deals', '')
        minimum_gross_commission = request.POST.get('minimum_gross_commission', '')
        maximum_gross_commission = request.POST.get('maximum_gross_commission', '')
        minimum_net_commission = request.POST.get('minimum_net_commission', '')
        maximum_net_commission = request.POST.get('maximum_net_commission', '')
        date_from = request.POST.get('from', '')
        date_to = request.POST.get('to', '')

        min_deals = int(minimum_deals) if minimum_deals else None
        max_deals = int(maximum_deals) if maximum_deals else None
        min_gross = float(minimum_gross_commission) if minimum_gross_commission else None
        max_gross = float(maximum_gross_commission) if maximum_gross_commission else None
        min_net = float(minimum_net_commission) if minimum_net_commission else None
        max_net = float(maximum_net_commission) if maximum_net_commission else None

        rental_qs = RentalDeals.objects.filter(is_deleted='N',account_id = request.user.account_id).prefetch_related('submitted_by_user')
        if agent_name:
            rental_qs = rental_qs.filter(submitted_by_user__name__icontains=agent_name)
        if deal_type and deal_type != 'Rental':
            rental_qs = rental_qs.none()
        if date_from:
            rental_qs = rental_qs.filter(date__gte=date_from)
        if date_to:
            rental_qs = rental_qs.filter(date__lte=date_to)

        sales_qs = SalesDeals.objects.filter(is_deleted='N', account_id = request.user.account_id).prefetch_related('submitted_by_user')
        if agent_name:
            sales_qs = sales_qs.filter(
                Q(agent_name1__icontains=agent_name) |
                Q(agent_name2__icontains=agent_name)
            )
        if deal_type and deal_type != 'Sales':
            sales_qs = sales_qs.none()
        if date_from:
            sales_qs = sales_qs.filter(date__gte=date_from)
        if date_to:
            sales_qs = sales_qs.filter(date__lte=date_to)

        rental_data = RentalDealsSerializer(rental_qs, many=True).data
        sales_data = SalesDealsSerializer(sales_qs, many=True).data
        combined_data = rental_data + sales_data

        search_value = request.POST.get('search[value]', '').strip().lower()
        if search_value:
            def matches_search(row):
                for key, value in row.items():
                    if value and search_value in str(value).lower():
                        return True
                return False
            combined_data = list(filter(matches_search, combined_data))

        groups = defaultdict(lambda: {'no_deals': 0, 'total_gross': 0.0, 'total_net': 0.0})
        for deal in combined_data:
            key = (deal['primary_agent'], deal['deal_type'])
            groups[key]['no_deals'] += 1
            # gross = float(deal['gross_commission'] or 0)
            # net = float(deal['net_commission'] or 0)
            gross = safe_float(deal.get('gross_commission'))
            net = safe_float(deal.get('net_commission')) 
            groups[key]['total_gross'] += gross
            groups[key]['total_net'] += net

        group_list = [
            {
                'agent_name': k[0],
                'deal_type': k[1],
                'no_deals': v['no_deals'],
                'total_gross_commission': round(v['total_gross'], 2),
                'total_net_commission': round(v['total_net'], 2)
            }
            for k, v in groups.items()
        ]

        def matches_filters(group):
            if min_deals is not None and group['no_deals'] < min_deals:
                return False
            if max_deals is not None and group['no_deals'] > max_deals:
                return False
            if min_gross is not None and group['total_gross_commission'] < min_gross:
                return False
            if max_gross is not None and group['total_gross_commission'] > max_gross:
                return False
            if min_net is not None and group['total_net_commission'] < min_net:
                return False
            if max_net is not None and group['total_net_commission'] > max_net:
                return False
            return True

        group_list = list(filter(matches_filters, group_list))

        order_column_idx = int(request.POST.get('order[0][column]', 0))
        order_dir = request.POST.get('order[0][dir]', 'asc')
        order_columns = [
            'agent_name', 'deal_type', 'no_deals',
            'total_gross_commission', 'total_net_commission'
        ]
        order_field = order_columns[order_column_idx]

        def sort_key(x):
            val = x.get(order_field)
            if order_field in ['no_deals']:
                return val or 0
            elif order_field in ['total_gross_commission', 'total_net_commission']:
                return val or 0.0
            return str(val or '').lower()

        group_list.sort(key=sort_key, reverse=(order_dir == 'desc'))

        page_data = group_list[start:start + length]

        return Response({
            'draw': draw,
            'recordsTotal': len(group_list),
            'recordsFiltered': len(group_list),
            'data': page_data
        }, status=status.HTTP_200_OK)