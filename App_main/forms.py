from django import forms
from App_main.models import *


class ProjectModelForm(forms.ModelForm):
    deadline = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = ProjectModel
        exclude = ['assigned_by', 'task_status']
