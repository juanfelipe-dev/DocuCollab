"""
Views for the docs application with role-based access control.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, JsonResponse, Http404
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.core.files.storage import default_storage
from django.conf import settings
import os
import json
import hashlib
import hmac
from datetime import datetime

from .models import Document, UserRole, DocumentPermission, DocumentVersion
from .forms import DocumentUploadForm, DocumentSearchForm, DocumentPermissionForm
from .permissions import (
    user_is_admin, user_is_manager, user_is_user,
    can_create_document, can_edit_document, can_delete_document,
    can_view_document, can_download_document, can_export_document,
    get_user_role
)


# ==================== Utility Functions ====================

def get_onlyoffice_config(document, user, is_edit):
    """Generate OnlyOffice configuration for document editing."""
    file_ext = document.get_file_extension()
    
    # Determine the document type for OnlyOffice
    doc_type_map = {
        'docx': 'text',
        'xlsx': 'spreadsheet',
        'pptx': 'presentation',
    }
    doc_type = doc_type_map.get(file_ext, 'text')
    
    config = {
        'documentType': doc_type,
        'document': {
            'title': document.title,
            'url': f"{settings.ONLYOFFICE_URL}/document/{document.id}/download/",
            'fileType': file_ext,
            'key': f"{document.id}-{document.updated_at.timestamp()}",
            'permissions': {
                'edit': is_edit,
                'download': True,
                'print': True,
            }
        },
        'editor': {
            'mode': 'edit' if is_edit else 'view',
            'callbackUrl': f"{settings.ONLYOFFICE_URL}/document/{document.id}/callback/",
        },
        'user': {
            'id': str(user.id),
            'name': user.get_full_name() or user.username,
        }
    }
    
    return config


# ==================== Authentication & Landing ====================

def index(request):
    """Landing page that redirects to appropriate view based on authentication."""
    if request.user.is_authenticated:
        return redirect('docs:docs_list')
    return redirect('login')


# ==================== Document Listing & Search ====================

@login_required
def docs_list(request):
    """List documents based on user role.

    Regular users should be able to *see* all documents (they are only
    prevented from creating/editing/deleting). The previous implementation
    filtered the queryset which meant ordinary users saw nothing unless a
    manager had explicitly shared a document with them.  Remove that
    restriction so everyone sees the full list.
    """
    user_role = get_user_role(request.user)
    documents = Document.objects.filter(is_archived=False)
    # we no longer apply additional filtering here; permissions are enforced
    # in the individual view/download/export endpoints.
    
    # Search functionality
    form = DocumentSearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data.get('query')
        file_type = form.cleaned_data.get('file_type')
        
        if query:
            documents = documents.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        
        if file_type:
            documents = documents.filter(file_type=file_type)
    
    context = {
        'documents': documents,
        'search_form': form,
        'user_role': user_role,
        'can_create': can_create_document(request.user),
        'can_delete': user_role in ['admin', 'manager'],
    }
    return render(request, 'docs/list.html', context)


# ==================== Document CRUD Operations ====================

@login_required
@require_http_methods(["GET", "POST"])
def create_document(request):
    """Create a new document.

    This view should not be accessible to regular users. We raise a
    404 error for those without creation rights so the endpoint effectively
    disappears for them, satisfying the requirement to remove the creation
    function for the "user" role.
    """
    if not can_create_document(request.user):
        # behave as if the URL does not exist
        raise Http404()

    
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.owner = request.user
            document.file_type = document.get_file_extension()
            document.save()
            
            # Create initial version
            DocumentVersion.objects.create(
                document=document,
                file=document.file,
                version_number=1,
                created_by=request.user,
                change_summary='Initial upload'
            )
            
            messages.success(request, f'Document "{document.title}" created successfully.')
            return redirect('docs:edit_document', pk=document.id)
    else:
        form = DocumentUploadForm()
    
    context = {'form': form}
    return render(request, 'docs/create.html', context)


@login_required
def edit_document(request, pk):
    """Edit a document with OnlyOffice integration."""
    document = get_object_or_404(Document, pk=pk)
    
    if not can_edit_document(request.user, document):
        messages.error(request, 'You do not have permission to edit this document.')
        return redirect('docs:docs_list')
    
    # Generate OnlyOffice config
    config = get_onlyoffice_config(document, request.user, is_edit=True)
    
    context = {
        'document': document,
        'config': json.dumps(config),
        'onlyoffice_url': settings.ONLYOFFICE_URL,
    }
    return render(request, 'docs/edit.html', context)


@login_required
def view_document(request, pk):
    """View a document in read-only mode."""
    document = get_object_or_404(Document, pk=pk)
    
    if not can_view_document(request.user, document):
        messages.error(request, 'You do not have permission to view this document.')
        return redirect('docs:docs_list')
    
    # Generate OnlyOffice config for view-only
    config = get_onlyoffice_config(document, request.user, is_edit=False)
    
    context = {
        'document': document,
        'config': json.dumps(config),
        'onlyoffice_url': settings.ONLYOFFICE_URL,
        'is_view_only': True,
    }
    return render(request, 'docs/view.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def delete_document(request, pk):
    """Delete a document."""
    document = get_object_or_404(Document, pk=pk)
    
    if not can_delete_document(request.user, document):
        messages.error(request, 'You do not have permission to delete this document.')
        return redirect('docs:docs_list')
    
    if request.method == 'POST':
        title = document.title
        document.delete()
        messages.success(request, f'Document "{title}" deleted successfully.')
        return redirect('docs:docs_list')
    
    context = {'document': document}
    return render(request, 'docs/confirm_delete.html', context)


# ==================== Download & Export ====================

@login_required
def download_document(request, pk):
    """Download a document."""
    document = get_object_or_404(Document, pk=pk)
    
    if not can_download_document(request.user, document):
        messages.error(request, 'You do not have permission to download this document.')
        return redirect('docs:docs_list')
    
    try:
        response = FileResponse(document.file.open('rb'))
        response['Content-Disposition'] = f'attachment; filename="{document.title}.{document.file_type}"'
        return response
    except FileNotFoundError:
        messages.error(request, 'File not found.')
        return redirect('docs:docs_list')


@login_required
def export_document(request, pk):
    """Export a document (download with metadata)."""
    document = get_object_or_404(Document, pk=pk)
    
    if not can_export_document(request.user, document):
        messages.error(request, 'You do not have permission to export this document.')
        return redirect('docs:docs_list')
    
    # For now, export is the same as download
    # But we can add metadata or convert format in the future
    return download_document(request, pk)


# ==================== Document Details & Metadata ====================

@login_required
def document_detail(request, pk):
    """Show document details and metadata."""
    document = get_object_or_404(Document, pk=pk)
    
    if not can_view_document(request.user, document):
        messages.error(request, 'You do not have permission to view this document.')
        return redirect('docs:docs_list')
    
    # Get document versions
    versions = document.versions.all()
    
    # Get document permissions
    permissions = document.permissions.all()
    
    # Get user role
    user_role = get_user_role(request.user)
    
    context = {
        'document': document,
        'versions': versions,
        'permissions': permissions,
        'user_role': user_role,
        'can_manage': can_delete_document(request.user, document),
    }
    return render(request, 'docs/detail.html', context)


# ==================== Permissions Management ====================

@login_required
@require_http_methods(["GET", "POST"])
def manage_permissions(request, pk):
    """Manage document permissions."""
    document = get_object_or_404(Document, pk=pk)
    
    # Only owner or admin can manage permissions
    user_role = get_user_role(request.user)
    if document.owner != request.user and user_role != 'admin':
        messages.error(request, 'You do not have permission to manage this document.')
        return redirect('docs:docs_list')
    
    if request.method == 'POST':
        # Add permission logic here
        pass
    
    context = {
        'document': document,
        'permissions': document.permissions.all(),
    }
    return render(request, 'docs/manage_permissions.html', context)


# ==================== API Endpoints ====================

@login_required
def api_document_list(request):
    """API endpoint for document list (JSON)."""
    user_role = get_user_role(request.user)
    documents = Document.objects.filter(is_archived=False)
    
    if user_role == 'user':
        documents = documents.filter(
            Q(owner=request.user) |
            Q(permissions__user=request.user)
        ).distinct()
    
    data = {
        'documents': [
            {
                'id': doc.id,
                'title': doc.title,
                'owner': doc.owner.username,
                'created_at': doc.created_at.isoformat(),
                'file_type': doc.file_type,
                'size': doc.get_file_size_mb(),
            }
            for doc in documents
        ]
    }
    return JsonResponse(data)
