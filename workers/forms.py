from django import forms
from . import models


class CreateWorkerForm(forms.ModelForm):

    class Meta:
        model = models.Worker
        fields = ['first_name', 'last_name', 'company']
        widgets = {
            'first_name': forms.Textarea(attrs={'class': 'form-control mb-4', 'rows': '1'}),
            'last_name': forms.Textarea(attrs={'class': 'form-control mb-4', 'rows': '1'}),
            'company': forms.Select(attrs={'class': 'form-control mb-4', 'rows': '1'}),
        }


class WorkerInfoForm(forms.ModelForm):

    class Meta:
        model = models.WorkerInfo
        fields = '__all__'
        widgets = {
            'worker': forms.Select(attrs={'class': 'form-control mb-4', 'rows': '1'}),
            'phone_num': forms.Textarea(attrs={'class': 'form-control mb-4', 'rows': '1'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-4', 'rows': '1'}),
            'citizenship': forms.Textarea(attrs={'class': 'form-control mb-4', 'rows': '1'}),
            'living_address': forms.Textarea(attrs={'class': 'form-control mb-4', 'rows': '1'}),
            'temporary_address': forms.Textarea(attrs={'class': 'form-control mb-4', 'rows': '1'}),
            'emso': forms.Textarea(attrs={'class': 'form-control mb-4', 'rows': '1'}),
            'tax_num': forms.Textarea(attrs={'class': 'form-control mb-4', 'rows': '1'}),
            'insurance_num': forms.Textarea(attrs={'class': 'form-control mb-4', 'rows': '1'}),
        }


class AssignedToProjectForm(forms.ModelForm):
    
    class Meta:
        model = models.AssignedToProject
        fields = ['project', 'worker', 'start_date', 'end_date']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control mb-4', 'rows': '1'}),
            'worker': forms.Select(attrs={'class': 'form-control mb-4', 'rows': '1'}),
            'start_date': forms.SelectDateWidget(attrs={'class': 'form-control', 'rows': '1'}),
            'end_date': forms.SelectDateWidget(attrs={'class': 'form-control', 'rows': '1'}),
        }
