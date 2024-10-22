# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Patient

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")


# forms.py

class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'dob', 'gender', 'address', 'phone', 'emergency_contact', 'insurance_provider', 'insurance_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # HTML5 date input
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency Contact'}),
            'insurance_provider': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insurance Provider'}),
            'insurance_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insurance Number'}),
        }
