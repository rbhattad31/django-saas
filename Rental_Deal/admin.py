from django.contrib import admin
from core.models import RentalDeals,Users
from django.contrib.auth.models import Group
from django import forms

# admin.site.register(RentalDeals)
# @admin.register(Users)
# class UsersAdmin(admin.ModelAdmin):
#     list_display =  ('id', "name",'password','email','get_groups')

#     def get_groups(self, obj):
#         return ", ".join([group.name for group in obj.groups.all()])
#     get_groups.short_description = 'Groups'

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

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from core.models import Users

# Form for creating users
class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ('email', 'name')  # Add fields as needed

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords don’t match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # ✅ Hashes password
        if commit:
            user.save()
        return user


# Form for updating users
class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()  # shows hashed password

    class Meta:
        model = Users
        fields = ('email', 'password', 'is_active', 'is_staff', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]  # Keep hashed password


# Custom admin
class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ("id",'email', 'is_staff', 'is_superuser','password','get_groups')
    list_filter = ('is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )

    ordering = ['email']
    search_fields = ('email',)
    filter_horizontal = ('groups', 'user_permissions')

    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    get_groups.short_description = 'Groups'

admin.site.register(Users, CustomUserAdmin)





