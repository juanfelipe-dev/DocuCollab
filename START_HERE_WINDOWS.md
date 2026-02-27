# 🚀 START HERE - DocuCollab Setup (Windows)

## What You Have
A complete Django collaborative document management system with user roles and OnlyOffice integration support.

## Get It Running (3 Steps - 5 Minutes)

### Step 1: Open Command Prompt
1. Press `Windows Key + R`
2. Type: `cmd`
3. Press Enter

### Step 2: Navigate & Run Setup
```bash
cd f:\Copilot Projects\DocuCollab
setup.bat
```

This automatically:
- Creates Python environment
- Installs packages
- Creates database
- Asks you to create admin account

**When asked "Username, Email, Password":**
```
Username: admin
Email: admin@example.com
Password: admin123
```

### Step 3: Start the App
```bash
python manage.py runserver
```

## Open Your Browser
Go to: **http://localhost:8000**

Login with:
- Username: `admin`
- Password: `admin123`

## That's IT! 🎉

You now have:
✅ Document management system
✅ User roles (Admin, Manager, User)
✅ Upload & download documents
✅ Share documents with others
✅ Admin panel at /admin
✅ Ready for OnlyOffice integration

## What to Do Next?

### Create Sample Data
In a new command prompt:
```bash
cd f:\Copilot Projects\DocuCollab
venv\Scripts\activate
python manage.py initializeapp
```

This creates:
- Manager user: manager / manager123
- Regular users: user1 / user123, user2 / user123

### Try Different Accounts
1. Logout (top right)
2. Login as `user1 / user123`
3. Try uploading (you can't - only managers can)
4. Try viewing shared documents
5. Try downloading

### Upload a Test Document
1. Login as `admin` or `manager`
2. Click "Documents" → "+ New Document"
3. Fill in:
   - Title: "My Document"
   - Choose a .docx or .xlsx file
4. Click "Upload Document"

### Run Forever
To keep the server running:
1. Don't close the command prompt
2. Press `Ctrl+C` to stop server
3. Run `python manage.py runserver` again to restart

## Troubleshooting

### Port 8000 Already in Use?
```bash
python manage.py runserver 8001
```
Then visit: http://localhost:8001

### Need to Recreate Database?
```bash
del db.sqlite3
python manage.py migrate
python manage.py initializeapp
```

### Setup Failed?
Make sure Python is installed:
```bash
python --version
```

Should show 3.8 or higher.

## File Locations

- **Uploaded documents**: `media/documents/`
- **Database**: `db.sqlite3`
- **Code**: `docs/` folder
- **Templates**: `templates/` folder
- **Admin panel**: http://localhost:8000/admin

## Key Files to Know

| File | Purpose |
|------|---------|
| `manage.py` | Django control |
| `docucollab/settings.py` | Configuration |
| `docs/models.py` | Database structure |
| `docs/views.py` | Logic |
| `templates/` | Web pages |

## Want More Info?

- **Quick Guide**: Open `QUICKSTART.md`
- **Setup Help**: Open `INSTALLATION.md`
- **Feature List**: Open `FEATURES.md`
- **Code Guide**: Open `DEVELOPMENT.md`
- **Full Overview**: Open `README.md`
- **All Docs**: Open `DOCUMENTATION_INDEX.md`

## Admin Panel Features

After starting the server:
1. Go to: http://localhost:8000/admin
2. Login with admin account
3. You can:
   - Create users
   - Assign roles
   - Manage documents
   - Control permissions
   - View versions

## User Roles Explained

### ADMIN
- Can do everything
- Manage users
- Access admin panel

### MANAGER
- Create documents
- Edit own documents
- Delete own documents
- Share documents
- NO admin panel access

### USER
- View shared documents
- Download documents
- NO create/edit/delete
- NO admin access

## API Endpoints (For Developers)

- `http://localhost:8000/documents/` (JSON list)
- `http://localhost:8000/documents/1/download/`
- `http://localhost:8000/documents/1/export/`

## Security Notes

🔒 This setup is for **local testing only**

For production:
- Change SECRET_KEY in settings.py
- Set DEBUG = False
- Use PostgreSQL (not SQLite)
- Setup HTTPS

## Need Help?

### Common Issues
1. **Python not found**: Install from python.org
2. **Port in use**: Use port 8001 instead
3. **Database error**: Delete db.sqlite3 and run migrate again
4. **Can't upload**: Check file is .docx or .xlsx

### Get Help
1. Check QUICKSTART.md
2. Check INSTALLATION.md
3. Check README.md

## Summary

```
1. Open Command Prompt
2. cd f:\Copilot Projects\DocuCollab
3. setup.bat
4. python manage.py runserver
5. Open http://localhost:8000
6. Done! 🎉
```

## More Setup Options

### Mac/Linux Users
Open Terminal and run:
```bash
cd f:\Copilot Projects\DocuCollab
chmod +x setup.sh
./setup.sh
```

### Docker Setup (Optional)
To add OnlyOffice (collaborative editing):
```bash
docker-compose up -d
```
Then update ONLYOFFICE_URL in settings.py

### Production Deployment
See INSTALLATION.md → Production Deployment section

---

**Ready?** 🚀

👉 Run: `setup.bat` then `python manage.py runserver`

👉 Visit: `http://localhost:8000`

👉 Login: `admin / admin123`

**Happy document managing!** 📄✨
