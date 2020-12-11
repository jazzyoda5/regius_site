from django import forms
from django.contrib.auth.forms import (UserCreationForm, 
PasswordChangeForm,
PasswordResetForm,
SetPasswordForm)
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'is_staff', 'password2']:
            self.fields[fieldname].help_text = None

        self.fields['password1'].widget = forms.PasswordInput(
            {'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(
            {'class': 'form-control'})
        self.fields['email'].widget = forms.EmailInput(
            {'class': 'form-control'})
        self.fields['is_staff'].widget = forms.CheckboxInput(
            {'class': 'form-check-input'})
        self.fields['first_name'].label = 'Ime'
        self.fields['last_name'].label = 'Priimek'
        self.fields['username'].label = 'Uporabniško ime'
        self.fields['email'].label = 'Email'
        self.fields['is_staff'].label = 'Uporabnik bo administrator'
        self.fields['password1'].label = 'Geslo'
        self.fields['password2'].label = 'Ponovi geslo'
        self.fields['password1'].help_text = """ 
        <ul class="password-help_text">
        <li>
        <p>Geslo mora biti dolgo vsaj 8 znakov</p>
        </li>
        <li>
        <p>Geslo mora vsebovati črke in številke</p>
        </li>
        <li>
        <p>Geslo ne sme biti preveč podobno vašim osebnim podatkom</p>
        </li>
        </ul>
        """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2', 'is_staff']
        widgets = {
            'first_name': forms.Textarea(attrs={'class': 'form-control', 'rows': '1'}),
            'last_name': forms.Textarea(attrs={'class': 'form-control', 'rows': '1'}),
            'username': forms.Textarea(attrs={'class': 'form-control', 'rows': '1'}),
        }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username',
            'email'
        ]
        widgets = {
            'first_name': forms.Textarea(attrs={'class': 'form-control', 'rows': '1'}),
            'last_name': forms.Textarea(attrs={'class': 'form-control', 'rows': '1'}),
            'username': forms.Textarea(attrs={'class': 'form-control', 'rows': '1'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'rows': '1'}),
        }

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}))

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Staro geslo'
        self.fields['new_password1'].label = 'Novo geslo'
        self.fields['new_password2'].label = 'Ponovi novo geslo'

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


class ResetPasswordForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = 'Email'
        self.fields['email'].widget = forms.EmailInput(
            {'class': 'form-control'})
 
    class Meta:
        fields = '__all__'


class PasswordSetForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(PasswordSetForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = 'Novo geslo'
        self.fields['new_password1'].widget = forms.PasswordInput(
            {'class': 'form-control'})
        self.fields['new_password2'].label = 'Potrditev gesla'
        self.fields['new_password2'].widget = forms.PasswordInput(
            {'class': 'form-control'})
        self.fields['new_password1'].help_text = """ 
        <ul class="password-help_text">
        <li>
        <p>Geslo mora biti dolgo vsaj 8 znakov</p>
        </li>
        <li>
        <p>Geslo mora vsebovati črke in številke</p>
        </li>
        <li>
        <p>Geslo ne sme biti preveč podobno vašim osebnim podatkom</p>
        </li>
        </ul>
        """
 
    class Meta:
        fields = '__all__'

