# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import RentalDeals


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


        

class RentalDealForm(forms.ModelForm):
    class Meta:
        model = RentalDeals
        fields = '__all__' 

    def __init__(self, *args, **kwargs):
        super(RentalDealForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
        # Add form-control and mandetory_field class to every field
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing_classes} form-control mandetory_field'.strip()

class FinanceCommentForm(forms.ModelForm):
    class Meta:
        model = RentalDeals
        fields = ['comments_finance']
        widgets = {
            'comments_finance': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'comments_finance',
                'rows': 5,
                'placeholder': 'Finance Comments'
            })
        }