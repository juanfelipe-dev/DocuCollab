"""
Admin configuration for docs app.
"""
from django.contrib import admin
from .models import Document, UserRole, DocumentPermission, DocumentVersion


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'created_at', 'updated_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'file_type', 'created_at', 'updated_at', 'is_archived']
    list_filter = ['file_type', 'created_at', 'is_archived']
    search_fields = ['title', 'description', 'owner__username']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Document Info', {
            'fields': ('title', 'description', 'file', 'file_type')
        }),
        ('Ownership', {
            'fields': ('owner', 'last_modified_by')
        }),
        ('Status', {
            'fields': ('is_archived',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DocumentPermission)
class DocumentPermissionAdmin(admin.ModelAdmin):
    list_display = ['document', 'user', 'permission_type', 'granted_at']
    list_filter = ['permission_type', 'granted_at']
    search_fields = ['document__title', 'user__username']
    readonly_fields = ['granted_at']


@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = ['document', 'version_number', 'created_by', 'created_at']
    list_filter = ['created_at', 'document']
    search_fields = ['document__title', 'created_by__username']
    readonly_fields = ['created_at']
