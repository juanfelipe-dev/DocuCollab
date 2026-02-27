# DocuCollab - Collaborative Document Management System

A Django-based collaborative document management system with integrated support for OnlyOffice and Collabora for real-time collaborative editing.

## Features

- **Supported Document Formats**: Word (.docx), Excel (.xlsx)
- **Document Management**: Create, Edit, Delete, Export, Download, View (read-only)
- **Role-Based Access Control**:
  - **ADMIN** (Superuser): All actions available
  - **MANAGER**: Create, Edit, Delete documents
  - **COMMON USER**: Search, View documents (read-only), Download, Export
- **Collaborative Editing**: Integration-ready for OnlyOffice or Collabora
- **Document Permissions**: Share documents with specific access levels
- **Version Tracking**: Monitor document versions and change history
- **Minimal UI**: Clean, responsive interface built with HTML and CSS

## System Requirements

- Python 3.8+
- Django 4.2+
- SQLite3 (default) or PostgreSQL/MySQL
- Optional: OnlyOffice or Collabora for collaborative editing

## Installation & Setup

### 1. Clone the Repository

```bash
cd f:\Copilot Projects\DocuCollab
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account with username and password.

### 6. Assign User Roles

Admin users can assign roles to other users via the Django admin panel:

```bash
python manage.py runserver
# Navigate to http://localhost:8000/admin
# Go to "User Roles" to assign roles (Admin, Manager, User)
```

### 7. Start Development Server

```bash
python manage.py runserver
```

Access the application at: `http://localhost:8000`

## Quick Start

### Creating Your First Document

1. Login with your admin account
2. Navigate to "Documents"
3. Click "+ New Document"
4. Upload a Word (.docx) or Excel (.xlsx) file
5. Document appears in the list

### Managing Permissions

1. View a document's details
2. Click "Manage Permissions"
3. Grant access to other users with specific permission levels:
   - **View Only**: Read-only access
   - **Edit**: Can edit the document
   - **Manage**: Full control including permission management

## User Roles & Permissions

### ADMIN (Superuser)
- ✅ Create documents
- ✅ Edit all documents
- ✅ Delete all documents
- ✅ Download all documents
- ✅ Export all documents
- ✅ View all documents
- ✅ Manage all permissions
- ✅ Access admin panel

### MANAGER
- ✅ Create documents
- ✅ Edit own/shared documents
- ✅ Delete own documents
- ✅ Download documents
- ✅ Export documents
- ✅ View documents
- ❌ Cannot access admin panel

### COMMON USER
- ❌ Cannot create documents
- ❌ Cannot edit documents
- ❌ Cannot delete documents
- ✅ Can search documents
- ✅ Can view shared documents
- ✅ Can download documents
- ✅ Can export documents

## Folder Structure

```
DocuCollab/
├── docucollab/               # Project settings
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
├── docs/                     # Main app
│   ├── migrations/          # Database migrations
│   ├── __init__.py
│   ├── admin.py             # Admin configuration
│   ├── forms.py             # Django forms
│   ├── models.py            # Database models
│   ├── permissions.py       # Permission checking utilities
│   ├── urls.py              # App URL routing
│   └── views.py             # View functions
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── auth/
│   │   └── login.html       # Login page
│   └── docs/
│       ├── list.html        # Document list
│       ├── create.html      # Create/upload document
│       ├── edit.html        # Edit document
│       ├── view.html        # View document (read-only)
│       ├── detail.html      # Document details
│       ├── confirm_delete.html
│       └── manage_permissions.html
├── manage.py                # Django management script
└── requirements.txt         # Python dependencies
```

## Database Models

### UserRole
Stores user role assignments (Admin, Manager, User)

### Document
Core document model with metadata, file storage, and ownership info

### DocumentPermission
Manages document-level permissions for sharing

### DocumentVersion
Tracks document version history and changes

## OnlyOffice Integration (Optional)

To enable collaborative editing with OnlyOffice:

### 1. Install OnlyOffice Document Server

**Docker (Recommended)**:
```bash
docker run -i -t -d -p 8080:80 onlyoffice/documentserver:latest
```

**Or visit**: https://helpcenter.onlyoffice.com/installation/docs-developer-setup.aspx

### 2. Update Django Settings

Edit `docucollab/settings.py`:
```python
ONLYOFFICE_URL = 'http://localhost:8080'  # Your OnlyOffice instance URL
ONLYOFFICE_SECRET = 'your-secret-key'     # Set a secure secret key
```

### 3. Configure API Integration

The templates and views are already prepared for OnlyOffice integration. Once configured, the edit and view pages will display the collaborative editor.

### 4. Test the Integration

- Upload a document
- Click "Edit" to open the collaborative editor
- Make changes in real-time with other users

## Security Considerations

- Change `SECRET_KEY` in `settings.py` for production
- Set `DEBUG = False` in production
- Use HTTPS in production
- Configure `ALLOWED_HOSTS`
- Use environment variables for sensitive settings
- Implement CSRF protection (already enabled)
- Set up proper file upload validation

## API Endpoints

- `GET /documents/` - List documents (JSON)
- `GET /documents/<id>/download/` - Download document
- `GET /documents/<id>/export/` - Export/download document

## Troubleshooting

### Can't upload documents
- Check file permissions on `media/` folder
- Ensure file extension is `.docx` or `.xlsx`
- File size may be limited by Django settings

### Documents not appearing in list
- Check user role assignments in admin panel
- Verify user has "view" permission for shared documents
- Check if documents are archived

### OnlyOffice editor not loading
- Verify OnlyOffice is running and accessible
- Check `ONLYOFFICE_URL` setting matches your instance
- Check browser console for JavaScript errors
- Ensure document format is supported (docx, xlsx)

## Future Enhancements

- Real-time collaboration with WebSocket support
- Document search with full-text indexing
- Advanced permission granularity
- Document commenting and annotations
- Integration with other collaborative tools
- Audit logging for all document operations
- Document templates and workflows
- File format conversion
- Mobile app support

## License

MIT License - Feel free to use for personal or commercial projects

## Support

For issues or questions, please check the documentation or create an issue in the repository.

## Notes

- SQLite database (db.sqlite3) will be created on first migration
- Media files stored in `media/` directory
- Static files served from `static/` directory
- Admin panel available at `/admin/`
- Login required for all features except login page

---

**DocuCollab** - Making collaborative document management simple and accessible.
