# DocuCollab - Quick Start Guide

Get up and running in 5 minutes!

## Video Overview

This is a Django-based collaborative document management system with roles (Admin, Manager, User) and integration-ready for OnlyOffice.

## 5-Minute Setup (Windows)

### Step 1: Open Command Prompt
```bash
cd f:\Copilot Projects\DocuCollab
```

### Step 2: Run Setup Script
```bash
setup.bat
```

This script will:
1. Create virtual environment
2. Install dependencies
3. Create database
4. Create admin account

**When prompted for superuser:**
```
Username: admin
Email: admin@example.com
Password: admin123
```

### Step 3: Start Server
```bash
venv\Scripts\activate
python manage.py runserver
```

### Step 4: Initialize Sample Users (Optional)
In a new command prompt:
```bash
venv\Scripts\activate
cd f:\Copilot Projects\DocuCollab
python manage.py initializeapp
```

### Step 5: Open Browser
Go to: **http://localhost:8000**

## Login Credentials

If you ran `initializeapp`, use any of these:
- **Admin**: admin / admin123
- **Manager**: manager / manager123
- **User**: user1 / user123 (or user2 / user123)

## 5-Minute Setup (Mac/Linux)

```bash
cd f:\Copilot Projects\DocuCollab
chmod +x setup.sh
./setup.sh
```

Then follow Step 3-5 above.

## First Steps

### 1. Upload a Document
1. Login with admin account
2. Click "Documents" → "+ New Document"
3. Enter title: "Test Document"
4. Upload a .docx or .xlsx file
5. Click "Upload Document"

### 2. View the Document
1. Click "View" button in the list
2. See document details and metadata
3. Download button available

### 3. Edit Document
1. Click "Edit" button (Admin/Manager only)
2. See OnlyOffice placeholder
3. Download current version for offline editing

### 4. Test Different Roles
1. Logout (click your username → Logout)
2. Login as "user1/user123"
3. Notice:
   - No "+ New Document" button
   - Can only view own/shared documents
   - Different permissions

### 5. Manage Users (Admin Only)
1. Go to Admin: http://localhost:8000/admin
2. Login with admin account
3. Click "User Roles"
4. Create new user:
   - Go to Users section
   - Add User (e.g., "john")
   - Set password
5. Go back to User Roles
6. Create role for john → choose "manager"

## Features by User Role

### ADMIN (Superuser)
✅ Create documents
✅ Edit all documents
✅ Delete documents
✅ Share with anyone
✅ Manage user roles
✅ View all documents

### MANAGER
✅ Create documents
✅ Edit own documents
✅ Delete own documents  
✅ Share documents
❌ Manage users
❌ Edit others' documents

### USER (Common User)
✅ View shared documents
✅ Download documents
✅ Search documents
✅ Export documents
❌ Create documents
❌ Edit documents
❌ Delete documents

## What Each Button Does

| Button | What it does | Who can use |
|--------|-------------|-----------|
| + New Document | Upload new file | Admin, Manager |
| View | Read-only preview | Anyone with access |
| Edit | Open editor | Owner, assigned users |
| Download | Save to computer | Anyone with access |
| Delete | Remove document | Admin, Owner |
| Share | Grant access | Admin, Owner |
| Logout | Exit application | Everyone |

## File Types Supported

- ✅ Word Documents (.docx)
- ✅ Excel Spreadsheets (.xlsx)
- ❌ PDF, Images (not yet)

To add support, upload .docx or .xlsx files.

## Folder Structure

```
DocuCollab/
├── media/             ← Uploaded documents stored here
├── db.sqlite3         ← Database (created after setup)
├── manage.py          ← Django command tool
└── README.md          ← Full documentation
```

## Troubleshooting

### "Port 8000 is already in use"
```bash
python manage.py runserver 8001
```

### "Table does not exist" error
```bash
python manage.py migrate
```

### Can't login
- Make sure you created superuser in step 2
- Clear browser cookies (history)
- Try incognito/private mode

### Files not uploading
- Check file format: must be .docx or .xlsx
- Check file size: < 100 MB
- Check permissions on media/ folder

### Python not found
- Ensure Python is installed: `python --version`
- Make sure virtual environment is activated

## Next Steps

1. **Read Full Documentation**
   - Open README.md for detailed features
   - Check INSTALLATION.md for advanced setup

2. **Setup OnlyOffice** (Optional)
   - Enables live collaborative editing
   - Requires Docker: `docker-compose up -d`
   - Then update ONLYOFFICE_URL in settings

3. **Customize for Your Organization**
   - Change app title and colors
   - Add your logo
   - Create custom roles

4. **Deploy to Production**
   - Read INSTALLATION.md production section
   - Use PostgreSQL instead of SQLite
   - Configure HTTPS

## Key Files to Know

| File | Purpose |
|------|---------|
| settings.py | App configuration |
| models.py | Database structure |
| views.py | Request handlers |
| urls.py | URL routing |
| forms.py | Upload forms |
| permissions.py | Access control |
| templates/ | HTML pages |

## Commands Reference

```bash
# Start server
python manage.py runserver

# Stop server
Ctrl+C

# Open database shell
python manage.py dbshell

# Run Python shell
python manage.py shell

# Create admin account
python manage.py createsuperuser

# Initialize sample data
python manage.py initializeapp

# Create database backup
python manage.py dumpdata > backup.json

# Restore from backup
python manage.py loaddata backup.json
```

## Admin Panel Features

Access at: **http://localhost:8000/admin**

### Users
- Create new users
- Change passwords
- Set active/inactive

### User Roles
- Assign roles (Admin, Manager, User)
- View all role assignments

### Documents  
- View all documents
- See ownership and dates
- View file information

### Permissions
- Manage document sharing
- View access levels
- Revoke permissions

### Versions
- View version history
- See who made changes
- Track document evolution

## Security Notes

⚠️ For local testing only:
- Uses SQLite (not production-ready)
- DEBUG mode enabled
- Secret key is default

For production:
- Change SECRET_KEY
- Set DEBUG = False
- Use PostgreSQL
- Enable HTTPS
- Configure allowed hosts

## Support

Stuck? Check:
1. README.md - Feature overview
2. INSTALLATION.md - Detailed setup
3. DEVELOPMENT.md - Technical details
4. Admin panel help icons

## One-Liner Reference

```bash
# Everything in one command (Windows)
cd f:\Copilot Projects\DocuCollab && setup.bat

# Start app (after setup)
python manage.py runserver

# Initialize with users
python manage.py initializeapp

# Access app
# Open browser to http://localhost:8000
```

---

**That's it!** You now have a fully functional collaborative document management system. Start uploading documents and sharing with your team! 🚀

For more information, check README.md or INSTALLATION.md.
