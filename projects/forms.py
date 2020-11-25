from .models import Project, Client, ProjectAdress, ProjectContactInfo
from django import forms

class NewProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('__all__')
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
            'project_name': 'Ime projekta'
        }


class ProjectAddressForm(forms.ModelForm):

    class Meta:
        model = ProjectAdress
        fields = ['street', 'city', 'zip_code', 'country']
        widgets = {
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),            
        }


class ProjectContactInfoForm(forms.ModelForm):

    class Meta:
        model = ProjectContactInfo
        fields = '__all__'


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
            'name': 'Ime podjetja'
        }
