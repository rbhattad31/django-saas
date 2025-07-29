# from django.contrib import admin

# # Register your models here.

# from .models import Deal

# class DealAdmin(admin.ModelAdmin):
#     list_display = ('agent_name', 'reference_number', 'project_name', 'deal_date')
#     search_fields = ('agent_name', 'reference_number', 'project_name')
#     list_filter = ('deal_date',)

# admin.site.register(Deal, DealAdmin)
#from django.contrib import admin
# from .models import Property

# @admin.register(Property)
# class PropertyAdmin(admin.ModelAdmin):
#     list_display = (
#         'reference_number', 'agent_name', 'project_name',
#         'building_name', 'unit_no', 'deal_date'
#     )

# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import Users,RentalProperties
# from django import forms
# from django.forms import TextInput


# class CustomUserChangeForm(forms.ModelForm):
#     class Meta:
#         model = Users
#         fields = '__all__'
#         widgets = {
#             'email': TextInput(attrs={'size': '40'}),
#             'name': TextInput(attrs={'size': '40'}),
#         }


# class CustomUserAdmin(UserAdmin):
#     form = CustomUserChangeForm
#     model = Users

#     list_display = ('email', 'name', 'is_staff', 'is_active')
#     list_filter = ('is_staff', 'is_superuser', 'is_active')

#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal Info', {'fields': ('name', 'mobile_number', 'gender', 'dob', 'additional_info', 'timezone', 'image')}),
#         ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
#         ('System Info', {'fields': ('user_account_id', 'created_by', 'updated_by', 'is_deleted', 'remember_token')}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_active')}
#         ),
#     )

#     search_fields = ('email', 'name')
#     ordering = ('email',)


# admin.site.register(Users)


    

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from core.models import Users, RentalProperties,Account

# Optional: Custom form for Users (not mandatory unless you're editing user fields)
# class UsersAdmin(BaseUserAdmin):
#     model = Users
#     list_display = ('email', 'name', 'is_staff', 'is_superuser')
#     search_fields = ('email', 'name')
#     ordering = ('email',)
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal Info', {'fields': ('name', 'mobile_number', 'gender', 'dob')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important Dates', {'fields': ('last_login',)}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser')}
#         ),
#     )

# admin.site.register(Users, UsersAdmin)
# admin.site.register(Accounts)


# For RentalProperties (unmanaged model)
@admin.register(RentalProperties)
class RentalPropertiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_name', 'owner_first_name', 'deal_date')  # adjust as needed
    search_fields = ('project_name', 'owner_first_name', 'agent_name')
