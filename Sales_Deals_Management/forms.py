from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from core.models import SalesDeals

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class SalesDealsForm(forms.ModelForm):
    class Meta:
        model = SalesDeals
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract user from view
        super(SalesDealsForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        # Optional: Set fields as not required for drafts
        self.fields['submitted_by_user'].required = False
        self.fields['created_by'].required = False
        self.fields['is_deleted'].required = False
        self.fields['is_approved_rejected'].required = False
        self.fields['is_entered_in_finance_system'].required = False
        self.fields['date'].required = False

