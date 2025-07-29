# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm

# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

# class SignUpForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']


# custom user forms 

# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import Users
# from .models import RentalProperties


# # class LoginForm(forms.Form):
# #     email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
# #     password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))



# class LoginForm(forms.Form):
#     username = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 "placeholder": "Username",
#                 "class": "form-control"
#             }
#         ))
#     password = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 "placeholder": "Password",
#                 "class": "form-control"
#             }
#         ))

# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(
#         max_length=254,
#         help_text='Required. Enter a valid email address.',
#         widget=forms.EmailInput(attrs={'class': 'form-control'})
#     )

#     class Meta:
#         model = Users
#         fields = ('name', 'email', 'password1', 'password2')  # Removed 'role'
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
#             'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
#             'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
#         }


# # class PropertyForm(forms.ModelForm):
# #     class Meta:
# #         model = RentalProperties
# #         fields = '__all__'  # or list fields like ['property_name', 'status', ...]
# #         widgets = {
# #             'status': forms.Select(attrs={'class': 'form-control'}),
# #             'property_name': forms.TextInput(attrs={'class': 'form-control'}),
# #             # Add widgets for other fields here as needed
# #         }

# class PropertyForm(forms.ModelForm):
#     class Meta:
#         model = RentalProperties
#         fields = '__all__'  # Adjust fields as needed based on your model
#         widgets = {
#             'deal_date': forms.DateInput(attrs={'type': 'date'}),
#             'pm_start_date': forms.DateInput(attrs={'type': 'date'}),
#             'pm_end_date': forms.DateInput(attrs={'type': 'date'}),
#             'tenancy_start_date': forms.DateInput(attrs={'type': 'date'}),
#             'tenancy_end_date': forms.DateInput(attrs={'type': 'date'}),
#             'cheque_date': forms.DateInput(attrs={'type': 'date'}),
#             'aml': forms.RadioSelect(choices=[('Yes', 'Yes'), ('No', 'No')]),
#             'approve_reject': forms.RadioSelect(choices=[('Approve', 'Approve'), ('Reject', 'Reject'), ('Waiting for Finance', 'Waiting for Finance')]),
#         }

