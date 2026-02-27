"""
Permission checking utilities for role-based access control.
"""
from .models import UserRole, DocumentPermission


def get_user_role(user):
    """Get user role (admin, manager, or user)."""
    if not user.is_authenticated:
        return None
    
    if user.is_superuser:
        return 'admin'
    
    try:
        user_role = UserRole.objects.get(user=user)
        return user_role.role
    except UserRole.DoesNotExist:
        return 'user'


def user_is_admin(user):
    """Check if user is admin."""
    return user.is_superuser or get_user_role(user) == 'admin'


def user_is_manager(user):
    """Check if user is manager or above."""
    role = get_user_role(user)
    return role in ['admin', 'manager']


def user_is_user(user):
    """Check if user is regular user or above."""
    role = get_user_role(user)
    return role in ['admin', 'manager', 'user']


def can_create_document(user):
    """Check if user can create documents."""
    if not user.is_authenticated:
        return False
    
    role = get_user_role(user)
    return role in ['admin', 'manager']


def can_edit_document(user, document):
    """Check if user can edit a document."""
    if not user.is_authenticated:
        return False
    
    role = get_user_role(user)
    
    # Admin can edit any document
    if role == 'admin':
        return True
    
    # Owner can edit their own document
    if document.owner == user:
        return True
    
    # Check document permissions
    try:
        permission = DocumentPermission.objects.get(document=document, user=user)
        return permission.can_edit()
    except DocumentPermission.DoesNotExist:
        return False


def can_delete_document(user, document):
    """Check if user can delete a document."""
    if not user.is_authenticated:
        return False
    
    role = get_user_role(user)
    
    # Admin can delete any document
    if role == 'admin':
        return True
    
    # Manager and owner can delete documents they own
    if role == 'manager' and document.owner == user:
        return True
    
    return False


def can_view_document(user, document):
    """Check if user can view a document.

    All authenticated users are permitted to view any non-archived
    document; the role-based restrictions only apply to actions such as
    create/edit/delete.  This simplifies the user experience in the list
    view, which now shows all documents regardless of ownership.
    """
    if not user.is_authenticated:
        return False
    # any logged-in user may view
    return True


def can_download_document(user, document):
    """Check if user can download a document."""
    # Download allowed for anyone who can view
    return can_view_document(user, document)


def can_export_document(user, document):
    """Check if user can export a document."""
    # Export allowed for anyone who can download
    return can_download_document(user, document)

def can_manage_permissions(user, document):
    """Check if user can manage document permissions."""
    if not user.is_authenticated:
        return False
    
    role = get_user_role(user)
    
    # Admin can manage any document's permissions
    if role == 'admin':
        return True
    
    # Owner can manage their own document's permissions
    if document.owner == user:
        return True
    
    return False
