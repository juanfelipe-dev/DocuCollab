"""
URL configuration for docs app.
"""
from django.urls import path
from . import views

app_name = 'docs'

urlpatterns = [
    # Main pages
    path('', views.index, name='index'),
    path('documents/', views.docs_list, name='docs_list'),
    
    # Document operations
    path('documents/create/', views.create_document, name='create_document'),
    path('documents/<int:pk>/detail/', views.document_detail, name='document_detail'),
    path('documents/<int:pk>/edit/', views.edit_document, name='edit_document'),
    path('documents/<int:pk>/view/', views.view_document, name='view_document'),
    path('documents/<int:pk>/delete/', views.delete_document, name='delete_document'),
    
    # Download and export
    path('documents/<int:pk>/download/', views.download_document, name='download_document'),
    path('documents/<int:pk>/export/', views.export_document, name='export_document'),
    
    # Permissions
    path('documents/<int:pk>/permissions/', views.manage_permissions, name='manage_permissions'),
    
    # API endpoints
    path('api/documents/', views.api_document_list, name='api_document_list'),
]
