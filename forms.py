from django import forms
from django.contrib.auth.forms import AuthenticationForm

class BootstrapAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})

# Patch DocumentSearchForm for Bootstrap
class DocumentSearchForm(forms.Form):
    query = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search documents...'}))
    file_type = forms.ChoiceField(required=False, choices=[('', 'All Types'), ('docx', 'Word (.docx)'), ('xlsx', 'Excel (.xlsx)')], widget=forms.Select(attrs={'class': 'form-select'}))