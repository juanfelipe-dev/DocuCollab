"""
Forms for the docs application.
"""
from django import forms
from .models import Document, DocumentPermission


class DocumentUploadForm(forms.ModelForm):
    """Form for uploading documents."""
    class Meta:
        model = Document
        fields = ['title', 'description', 'file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Document Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description (optional)',
                'rows': 4
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.docx,.xlsx'
            }),
        }


class DocumentPermissionForm(forms.ModelForm):
    """Form for managing document permissions."""
    class Meta:
        model = DocumentPermission
        fields = ['permission_type']
        widgets = {
            'permission_type': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class DocumentSearchForm(forms.Form):
    """Form for searching documents."""
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search documents...'
        })
    )
    file_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Types')] + list(Document.FILE_TYPE_CHOICES),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )


# Form for document comments with Bootstrap styling
from .models import DocumentComment
class DocumentCommentForm(forms.ModelForm):
    class Meta:
        model = DocumentComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add a comment...',
                'rows': 3
            })
        }
