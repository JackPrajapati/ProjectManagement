from django import forms
from django.forms import ModelForm
from .models import Employee, Project
from functools import partial


class ProjectForm(ModelForm):
    DateInput = partial(forms.DateInput, {'class': 'datepicker'})

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['description'].help_text = 'Optional'
        self.fields['start_date'].help_text = 'Optional, format: DD/MM/YYYY'
        self.fields['end_date'].help_text = 'Optional, format: DD/MM/YYYY'

    start_date = forms.DateField(widget=forms.TextInput(attrs={
        'class': 'datepicker',
        'autocomplete': 'off',
    }))
    end_date = forms.DateField(widget=forms.TextInput(attrs={
        'class': 'datepicker',
        'autocomplete': 'off',
    }))

    class Meta:
        model = Project
        fields = ['name', 'description']


class EmployeeLoginForm(forms.ModelForm):

    class Meta():
        model = Employee
        fields = ('username', 'password')


class EmployeeRegisterationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = Employee
        fields = ('username', 'email', 'designation')

