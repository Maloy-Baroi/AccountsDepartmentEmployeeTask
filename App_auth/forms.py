from django import forms
from App_auth.models import *
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class EmployeeProfileModelForm(forms.ModelForm):
    Date_of_Birth = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    joining_date = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = EmployeeProfileModel
        fields = "__all__"
