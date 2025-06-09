# from django.contrib import admin

# # Register your models here.

# from .models import Deal

# class DealAdmin(admin.ModelAdmin):
#     list_display = ('agent_name', 'reference_number', 'project_name', 'deal_date')
#     search_fields = ('agent_name', 'reference_number', 'project_name')
#     list_filter = ('deal_date',)

# admin.site.register(Deal, DealAdmin)
from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'reference_number', 'agent_name', 'project_name',
        'building_name', 'unit_no', 'deal_date'
    )
    

