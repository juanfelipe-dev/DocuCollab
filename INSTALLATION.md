# DocuCollab Installation Guide

Complete step-by-step guide to set up and run the DocuCollab application.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)
- Optional: Docker (for OnlyOffice setup)

## Installation Steps

### 1. Clone or Download the Project

```bash
cd f:\Copilot Projects\DocuCollab
```

### 2. Create and Activate Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Django 4.2.8 - Web framework
- python-decouple 3.8 - Environment variable management
- Pillow 10.1.0 - Image processing

### 4. Create Database Tables

```bash
python manage.py migrate
```

This creates the SQLite database (db.sqlite3) and all required tables:
- User and UserRole
- Document, DocumentPermission, DocumentVersion
- Django built-in tables for auth and sessions

### 5. Create Admin Account

```bash
python manage.py createsuperuser
```

Example:
```
Username: admin
Email: admin@example.com
Password: (enter password)
```

### 6. Initialize Sample Data (Optional)

Create sample users for testing with different roles:

```bash
python manage.py initializeapp
```

This creates:
- admin / admin123 - Admin user with all permissions
- manager / manager123 - Manager user (create, edit, delete)
- user1 / user123 - Regular user (view, download, export only)
- user2 / user123 - Regular user (view, download, export only)

### 7. Start Development Server

```bash
python manage.py runserver
```

Output will show:
```
Starting development server at http://127.0.0.1:8000/
```

## Quick Setup Script

Instead of manual steps, you can use the provided setup scripts:

**Windows:**
```bash
setup.bat
```

**Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

## Accessing the Application

### Main Application
- URL: `http://localhost:8000`
- Login required
- Default accounts from initialization (if ran)

### Admin Panel
- URL: `http://localhost:8000/admin`
- Requires superuser/admin account
- Manage users, roles, documents, permissions

## Testing the Application

### 1. Login

1. Go to `http://localhost:8000`
2. Click "Login"
3. Enter credentials (admin/admin123 or other accounts)

### 2. Create a Document

1. Click "Documents" in navbar
2. Click "+ New Document" (only available for Admin/Manager)
3. Fill in:
   - Title: "Test Document"
   - Description: "Test description"
   - File: Choose a .docx or .xlsx file
4. Click "Upload Document"

### 3. View Document

1. In documents list, click "View" on any document
2. See document details and metadata
3. Download option available

### 4. Edit Document

1. Click "Edit" on your own document (Admin/Manager only)
2. See editor placeholder
3. Use "Download Current Version" for manual editing

### 5. Share Documents

1. Go to document detail page
2. Click "Manage Permissions"
3. Grant access to other users (Feature under development)

### 6. Manage Permissions

1. Admin panel → User Roles
2. Assign roles to users:
   - Admin: Full access
   - Manager: Create, edit, delete
   - User: View, download, export only

## User Roles & Capabilities

### ADMIN
- All CRUD operations
- Access admin panel
- Manage all users and permissions
- View all documents

### MANAGER
- Create new documents
- Edit/delete own documents
- Share documents with others
- View shared documents
- Cannot access admin panel

### USER
- View documents (if shared)
- Download documents
- Export documents
- Search documents
- Cannot create/edit/delete

## OnlyOffice Integration (Optional)

### Using Docker (Recommended)

**Prerequisite:** Docker installed

1. Start OnlyOffice container:
```bash
docker-compose up -d
```

2. Update settings in `docucollab/settings.py`:
```python
ONLYOFFICE_URL = 'http://localhost:8080'
ONLYOFFICE_SECRET = 'your-secret-key'
```

3. Restart Django server:
```bash
python manage.py runserver
```

4. Edit pages will now show OnlyOffice editor

### Manual Installation

Visit: https://helpcenter.onlyoffice.com/installation/docs-developer-setup.aspx

After installation:
- Update ONLYOFFICE_URL in settings
- Restart server
- Edit/view pages will display editor

## File Structure Important Directories

```
media/               - Uploaded documents
documents/          - Document files
  document_versions/ - Version history

static/             - CSS, JS, images
                     (for production use)

db.sqlite3          - SQLite database
venv/               - Virtual environment (local)
```

## Configuration

### Settings File: `docucollab/settings.py`

Key settings to customize:

```python
# Security
SECRET_KEY = 'django-insecure-...'  # Change in production
DEBUG = True                          # Set False in production
ALLOWED_HOSTS = ['*']                 # Specify in production

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# OnlyOffice
ONLYOFFICE_URL = 'http://localhost:8080'
ONLYOFFICE_SECRET = 'your-secret-key'

# File Upload Limits
MAX_UPLOAD_SIZE = 104857600  # 100 MB in bytes (add to settings if needed)
```

## Troubleshooting

### Port 8000 Already in Use

Use a different port:
```bash
python manage.py runserver 8001
```

### Database Locked Error

Delete and recreate the database:
```bash
rm db.sqlite3
python manage.py migrate
python manage.py initializeapp
```

### Permission Denied on Files

On Linux/Mac, ensure media directory permissions:
```bash
chmod -R 755 media/
```

### Import Errors

Verify virtual environment is activated:
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### OnlyOffice Not Loading

1. Check if container is running:
```bash
docker ps | grep onlyoffice
```

2. Verify URL in settings matches container URL

3. Check browser console for JavaScript errors

## Production Deployment

### Before Going Live

1. **Change SECRET_KEY**
   - Generate new key: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - Update in settings.py

2. **Set DEBUG = False**
   - Hide stack traces in errors

3. **Configure ALLOWED_HOSTS**
   - Add your domain names

4. **Use PostgreSQL**
   - SQLite not recommended for production
   - Update DATABASES in settings.py

5. **Setup HTTPS**
   - Use SSL certificates
   - Set SECURE_SSL_REDIRECT = True

6. **Collect Static Files**
   ```bash
   python manage.py collectstatic
   ```

7. **Use Production Server**
   - Gunicorn, uWSGI, or similar
   - Don't use development server

### Deployment Example (Ubuntu/Linux)

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn docucollab.wsgi:application --bind 0.0.0.0:8000
```

## Support & Documentation

- Django Docs: https://docs.djangoproject.com/
- OnlyOffice Docs: https://api.onlyoffice.com/
- Python Docs: https://docs.python.org/3/

## Next Steps

1. Read the main README.md for feature overview
2. Explore the admin panel at /admin/
3. Create and test documents
4. Setup OnlyOffice for collaborative editing
5. Customize templates for your branding

## Need Help?

- Check FAQ section in README.md
- Review model documentation in models.py
- Check view functions in views.py
- Review permission logic in permissions.py

---

**Happy Documenting!** 🚀
