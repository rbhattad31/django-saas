from django.contrib import admin
from .models import RentalDeals

# admin.site.register(RentalDeals)

@admin.register(RentalDeals)
class RentalDealAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'date',
        'deal_start_date',
        'reference_number', 
        'is_new_deal',
        'project_name',
        'submitted_by_user',
    )

