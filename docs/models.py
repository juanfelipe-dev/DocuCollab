"""
Models for the docs application.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone

class UserRole(models.Model):
    """User role model for managing user roles and permissions."""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('user', 'User'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_role')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['role', 'user__username']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_manager(self):
        return self.role == 'manager'
    
    def is_user(self):
        return self.role == 'user'


class Document(models.Model):
    """Document model for collaborative editing."""
    FILE_TYPE_CHOICES = [
        ('docx', 'Word (.docx)'),
        ('xlsx', 'Excel (.xlsx)'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(
        upload_to='documents/',
        validators=[FileExtensionValidator(allowed_extensions=['docx', 'xlsx'])]
    )
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    
    # Tracking fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='modified_documents'
    )
    
    # Status tracking
    is_archived = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner', '-created_at']),
            models.Index(fields=['title']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_file_size_mb(self):
        """Get file size in MB."""
        if self.file:
            return round(self.file.size / (1024 * 1024), 2)
        return 0
    
    def get_file_extension(self):
        """Get file extension."""
        return self.file.name.split('.')[-1].lower()


class DocumentPermission(models.Model):
    """Document-level permissions for collaborative editing."""
    PERMISSION_CHOICES = [
        ('view', 'View Only'),
        ('edit', 'Edit'),
        ('manage', 'Manage'),
    ]
    
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='permissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document_permissions')
    permission_type = models.CharField(
        max_length=10, 
        choices=PERMISSION_CHOICES,
        default='view'
    )
    granted_at = models.DateTimeField(auto_now_add=True)
    granted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='permissions_granted'
    )
    
    class Meta:
        unique_together = ('document', 'user')
        ordering = ['user__username']
    
    def __str__(self):
        return f"{self.document.title} - {self.user.username} ({self.permission_type})"
    
    def can_view(self):
        return self.permission_type in ['view', 'edit', 'manage']
    
    def can_edit(self):
        return self.permission_type in ['edit', 'manage']
    
    def can_manage(self):
        return self.permission_type == 'manage'


class DocumentVersion(models.Model):
    """Document version history for tracking changes."""
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='versions')
    file = models.FileField(upload_to='document_versions/')
    version_number = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    change_summary = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-version_number']
        unique_together = ('document', 'version_number')
    
    def __str__(self):
        return f"{self.document.title} v{self.version_number}"


# DocumentComment model for document comments
class DocumentComment(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.document.title}"
