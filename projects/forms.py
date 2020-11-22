from .models import Project, Client, ProjectAdress
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
            'contract_value': forms.TextInput(attrs={'class': 'form-control'}),
            'contract_num': forms.TextInput(attrs={'class': 'form-control'}),
            'hourly_rate': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'client': 'Stranka',
            'project_name': 'Ime projekta'
        }


# class NewClientForm(forms.class Form(forms.ModelForm):
