from django.contrib import admin
from .models import Rental_Deal

# admin.site.register(Rental_Deal)

@admin.register(Rental_Deal)
class RentalDealAdmin(admin.ModelAdmin):
    list_display = (
        'reference_number',
        'agent',
        'deal_type',
        'project_name',
        'unit_number',
        'building_name',
        'deal_start_date',
        'deal_end_date',
        'status',
        'created_at',
        'updated_at',
    )

