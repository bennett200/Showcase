from django import forms
from django.forms import HiddenInput

from .models import Email

class EmailBaseForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = '__all__'
    
    