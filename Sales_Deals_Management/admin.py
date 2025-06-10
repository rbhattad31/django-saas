from django.contrib import admin
from .models import SalesDeal

@admin.register(SalesDeal)
class SalesDealAdmin(admin.ModelAdmin):
    list_display = [
        'reference_number',
        'deal_submitted_by_agent',
        'submitted_date',
        'unit_no',
        'building_name',
        'project_name', # Only include if added to model
    ]

    list_filter = ['submitted_date', 'building_name', 'project_name']

    ordering = ['-submitted_date']
