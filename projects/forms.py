from .models import (Project, 
Client, 
ProjectAdress, 
ProjectContactInfo,
ProjectAnex)
from django import forms

class NewProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = [
            'client',
            'status',
            'project_name',
            'contractor',
            'contract_num',
            'project_start_date',
            'project_end_date',
            'contract_value',
            'hourly_rate'
        ]
        widgets = {
            'project_start_date': forms.SelectDateWidget(attrs={'class': 'form-control'}),
            'project_end_date': forms.SelectDateWidget(attrs={'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'contractor': forms.Select(attrs={'class': 'form-control'}),
            'project_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contract_num': forms.TextInput(attrs={'class': 'form-control'}),
            'contract_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0,25'}),
            'contract_num': forms.TextInput(attrs={'class': 'form-control'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0,25'}),
        }
        labels = {
            'client': 'Stranka',
            'project_name': 'Ime projekta',
            'contractor': 'Izvajalec'
        }


class ProjectAddressForm(forms.ModelForm):

    class Meta:
        model = ProjectAdress
        fields = ['project', 'street', 'city', 'zip_code', 'country']
        widgets = {
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),  
            'project': forms.Select(attrs={'class': 'form-control'}),           
        }
        labels = {
            'project': 'Projekt'
        }


class ProjectContactInfoForm(forms.ModelForm):

    class Meta:
        model = ProjectContactInfo
        fields = '__all__'
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'resp_client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'resp_client_phone_num': forms.TextInput(attrs={'class': 'form-control'}),
            'resp_client_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'resp_contractor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'resp_contractor_phone_num': forms.TextInput(attrs={'class': 'form-control'}),
            'resp_contractor_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'resp_on_site_name': forms.TextInput(attrs={'class': 'form-control'}),
            'resp_on_site_phone_num': forms.TextInput(attrs={'class': 'form-control'}),
            'resp_on_site_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'client_contract_signer': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'resp_client_name': 'Odgovorna oseba za pogodbo s strani naročnika',
            'resp_client_phone_num': 'Telefon',
            'resp_client_email': 'Email',
            'resp_contractor_name': 'Odgovorna oseba za pogodbo s strani izvajalca',
            'resp_contractor_phone_num': 'Telefon',
            'resp_contractor_email': 'Email',
            'resp_on_site_name': 'Projektni vodja s strani izvajalca',
            'resp_on_site_phone_num': 'Telefon',
            'resp_on_site_email': 'Email',
        }


class NewClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'tax_num': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Ime podjetja',
        }


class NewAnexForm(forms.ModelForm):

    class Meta:
        model = ProjectAnex
        fields = [
            'project',
            'start',
            'end',
            'value'
        ]
        widgets = {
            'start': forms.SelectDateWidget(attrs={'class': 'form-control'}),
            'end': forms.SelectDateWidget(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0,25'}),
            'project': forms.HiddenInput()
        }

