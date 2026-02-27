# DocuCollab Development Guide

A comprehensive guide for understanding and extending the DocuCollab codebase.

## Architecture Overview

DocuCollab follows the standard Django MVT (Model-View-Template) architecture:

```
User Request
    ↓
URL Router (urls.py)
    ↓
View Function (views.py)
    ↓
Permission Check (permissions.py)
    ↓
Database Query (models.py)
    ↓
Template Rendering (templates/)
    ↓
HTML Response to Browser
```

## Project Structure

```
DocuCollab/
├── docucollab/              # Project configuration
│   ├── settings.py         # Django settings & configuration
│   ├── urls.py             # Main URL router
│   └── wsgi.py             # WSGI configuration
│
├── docs/                    # Main application
│   ├── admin.py            # Admin panel configuration
│   ├── forms.py            # HTML form definitions
│   ├── models.py           # Database models
│   ├── permissions.py      # Permission/authorization logic
│   ├── urls.py             # App URL routing
│   ├── views.py            # Request handlers
│   └── management/         # Custom commands
│       └── commands/
│           └── initializeapp.py
│
├── templates/              # HTML templates
│   ├── base.html          # Base template with navigation
│   ├── auth/              # Authentication templates
│   │   └── login.html
│   └── docs/              # Document templates
│       ├── create.html
│       ├── edit.html
│       ├── list.html
│       ├── view.html
│       ├── detail.html
│       ├── confirm_delete.html
│       └── manage_permissions.html
│
├── media/                 # User-uploaded files
│   └── documents/        # Document uploads
│
├── static/               # Static files (CSS, JS, images)
├── manage.py             # Django CLI
├── requirements.txt      # Python dependencies
├── README.md             # Project overview
├── INSTALLATION.md       # Setup instructions
├── DEVELOPMENT.md        # This file
└── docker-compose.yml    # Docker configuration
```

## Core Models

### UserRole
```python
class UserRole(models.Model):
    user = OneToOneField(User)
    role = CharField(['admin', 'manager', 'user'])
```
- Associates a role with each user
- Used for permission checks
- Admins have `user.is_superuser = True`

### Document
```python
class Document(models.Model):
    title = CharField()
    file = FileField(upload_to='documents/')
    owner = ForeignKey(User)
    file_type = CharField(['docx', 'xlsx'])
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```
- Core model for documents
- Stores file metadata
- Tracks ownership and modification times

### DocumentPermission
```python
class DocumentPermission(models.Model):
    document = ForeignKey(Document)
    user = ForeignKey(User)
    permission_type = CharField(['view', 'edit', 'manage'])
```
- Controls document-level access
- Allows sharing with specific users
- Three permission levels: view, edit, manage

### DocumentVersion
```python
class DocumentVersion(models.Model):
    document = ForeignKey(Document)
    file = FileField()
    version_number = IntegerField()
    created_by = ForeignKey(User)
    change_summary = TextField()
```
- Tracks document evolution
- Stores previous versions
- Enables version history

## Views Overview

### Document Listing & Search
```python
docs_list()
```
- Shows documents user can access
- Filters by role and permissions
- Supports search and filtering

### CRUD Operations

**Create**
```python
create_document()  # POST multipart/form-data
```
- Only Admin/Manager can create
- Validates file type (.docx, .xlsx)
- Creates initial version record

**Read**
```python
view_document()    # Read-only view
edit_document()    # EditorMode
document_detail()  # Metadata view
```

**Update**
```python
edit_document()    # Update via OnlyOffice
```
- Redirects to OnlyOffice editor
- Updates last_modified_by
- Creates version record on save

**Delete**
```python
delete_document()  # Confirmation + deletion
```
- Soft delete option available
- Removes all associated versions
- Cascade deletes permissions

### File Operations

**Download**
```python
download_document()  # Returns FileResponse
```
- Streams file from disk
- Sets proper HTTP headers
- Checks view permission

**Export**
```python
export_document()    # Download alternative
```
- Currently same as download
- Future: format conversion

## Permission System

Located in `permissions.py`:

### Helper Functions
```python
get_user_role(user) → 'admin' | 'manager' | 'user'
user_is_admin(user) → bool
user_is_manager(user) → bool
user_is_user(user) → bool
```

### Permission Checks
```python
can_create_document(user)
can_edit_document(user, document)
can_delete_document(user, document)
can_view_document(user, document)
can_download_document(user, document)
can_manage_permissions(user, document)
```

### Permission Logic

1. **Superuser Check**: `user.is_superuser` → Always True
2. **Role Check**: Verify user role from UserRole model
3. **Ownership Check**: `document.owner == user` → Always granted
4. **Permission Check**: Query DocumentPermission table

Example:
```python
def can_edit_document(user, document):
    # Admins can edit anything
    if user_is_admin(user):
        return True
    
    # Owner can edit own document
    if document.owner == user:
        return True
    
    # Check shared permissions
    perm = DocumentPermission.objects.get(
        document=document, 
        user=user
    )
    return perm.permission_type in ['edit', 'manage']
```

## Forms

### DocumentUploadForm
- Title (required text)
- Description (optional textarea)
- File (required file upload)

### DocumentPermissionForm
- Permission type (choices: view, edit, manage)

### DocumentSearchForm
- Query (search text)
- File type (filter by docx/xlsx)

## Templates

### Base Template (`base.html`)
- Navigation bar
- CSS styling
- Message display
- Template blocks:
  - `{% block title %}`
  - `{% block content %}`
  - `{% block extra_css %}`

### Document Templates

**list.html** - Document listing with search
**create.html** - Upload form
**edit.html** - OnlyOffice editor placeholder
**view.html** - Read-only viewer
**detail.html** - Document metadata and versions
**confirm_delete.html** - Deletion confirmation
**manage_permissions.html** - Share document

## Extending the Application

### Adding a New Feature

1. **Add Model** (if needed)
```python
# In models.py
class DocumentComment(models.Model):
    document = ForeignKey(Document)
    user = ForeignKey(User)
    text = TextField()
    created_at = DateTimeField(auto_now_add=True)
```

2. **Create Migration**
```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Add Form** (if user input needed)
```python
# In forms.py
class DocumentCommentForm(forms.ModelForm):
    class Meta:
        model = DocumentComment
        fields = ['text']
```

4. **Add View**
```python
# In views.py
@login_required
def add_comment(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        form = DocumentCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.document = document
            comment.user = request.user
            comment.save()
    return redirect('document_detail', pk=pk)
```

5. **Add URL**
```python
# In urls.py
urlpatterns = [
    path('documents/<int:pk>/comment/', add_comment, name='add_comment'),
    # ...
]
```

6. **Add Template**
```html
<!-- In detail.html -->
{% if user.is_authenticated %}
<form method="post" action="{% url 'add_comment' document.id %}">
    {% csrf_token %}
    {{ form }}
    <button type="submit">Add Comment</button>
</form>
{% endif %}
```

7. **Register in Admin** (optional)
```python
# In admin.py
@admin.register(DocumentComment)
class DocumentCommentAdmin(admin.ModelAdmin):
    list_display = ['document', 'user', 'created_at']
```

### Modifying Permissions

Edit `permissions.py`:
```python
def can_comment_on_document(user, document):
    """New permission check"""
    if not user.is_authenticated:
        return False
    
    # Only users who can view can comment
    return can_view_document(user, document)
```

### Customizing Templates

Template CSS is in `<style>` block in `base.html`.

To customize styling:
1. Modify CSS in `base.html`
2. Or create `static/style.css` and link in template

Example custom class:
```css
.highlight-document {
    background: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 1rem;
}
```

## Authentication & Authorization

### Authentication
- Django's built-in authentication system
- User login via username/password
- Session-based (cookies)

### Authorization
- Custom permission system in `permissions.py`
- Checked in each view function
- Decorators: `@login_required`

###Role-Based Access Control (RBAC)
- Three roles: Admin, Manager, User
- Stored in UserRole model
- Checked via `get_user_role()`

## Database Queries

### Getting User Documents
```python
# User's own documents
documents = Document.objects.filter(owner=request.user)

# Shared documents
shared_docs = Document.objects.filter(
    permissions__user=request.user
)

# All accessible documents
accessible = Document.objects.filter(
    Q(owner=request.user) | 
    Q(permissions__user=request.user)
).distinct()
```

### Document Versions
```python
# Get specific version
version = DocumentVersion.objects.get(
    document=document,
    version_number=2
)

# Get all versions ordered
versions = document.versions.all()  # Already ordered
```

## Important Notes

### Security
- CSRF protection enabled
- File upload validation
- Field validation on forms
- SQL injection protection (ORM)

### Performance
- Index on `Document.owner` and `Document.created_at`
- Index on `Document.title` for search
- Use `select_related()` for FK lookups when needed

### File Handling
- Files stored in `media/documents/`
- Uploaded files validated by extension
- Max file size can be configured in settings

## Testing

### Run Admin Interface
```bash
python manage.py runserver
# Go to http://localhost:8000/admin
```

### Test with Different Users
1. Create users in admin panel
2. Assign roles via UserRole model
3. Login as each user to test permissions

### Monitor Database
```bash
# Django shell to query database
python manage.py shell
>>> from docs.models import Document
>>> Document.objects.all()
>>> Document.objects.filter(owner__username='admin')
```

## Common Tasks

### Add User Programmatically
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> from docs.models import UserRole
>>> user = User.objects.create_user('john', 'john@example.com', 'password')
>>> role = UserRole.objects.create(user=user, role='manager')
```

### Bulk Assign Role
```bash
python manage.py shell
>>> from docs.models import UserRole
>>> from django.contrib.auth.models import User
>>> users = User.objects.filter(username__startswith='user')
>>> for user in users:
...     UserRole.objects.get_or_create(user=user, defaults={'role': 'user'})
```

### Export Data
```bash
# Dump database
python manage.py dumpdata > backup.json

# Load database
python manage.py loaddata backup.json
```

## Debugging

### Enable Debug Output
```python
# In settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

### Print Queries
```python
from django.db import connection
# After code that runs queries
print(connection.queries)
```

## Further Learning

- Django Documentation: https://docs.djangoproject.com/
- Django Models: https://docs.djangoproject.com/en/4.2/topics/db/models/
- Django Views: https://docs.djangoproject.com/en/4.2/topics/http/views/
- Django Templates: https://docs.djangoproject.com/en/4.2/topics/templates/
- OnlyOffice API: https://api.onlyoffice.com/

---

**Happy Developing!** 🚀
