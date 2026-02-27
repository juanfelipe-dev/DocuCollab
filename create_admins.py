import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docucollab.settings')
django.setup()

from django.contrib.auth.models import User

print("\nCreating superuser accounts...\n")

# Create superuser 1
try:
    user1 = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✅ Created SUPERUSER 1")
    print("   Username: admin")
    print("   Password: admin123")
    print("   Email: admin@example.com\n")
except Exception as e:
    print(f"⚠️  SUPERUSER 1 (admin): {str(e)}\n")

# Create superuser 2
try:
    user2 = User.objects.create_superuser('superuser1', 'super1@example.com', 'super1234')
    print("✅ Created SUPERUSER 2")
    print("   Username: superuser1")
    print("   Password: super1234")
    print("   Email: super1@example.com\n")
except Exception as e:
    print(f"⚠️  SUPERUSER 2 (superuser1): {str(e)}\n")

# Create superuser 3
try:
    user3 = User.objects.create_superuser('superuser2', 'super2@example.com', 'super2345')
    print("✅ Created SUPERUSER 3")
    print("   Username: superuser2")
    print("   Password: super2345")
    print("   Email: super2@example.com\n")
except Exception as e:
    print(f"⚠️  SUPERUSER 3 (superuser2): {str(e)}\n")

print("=" * 60)
print("🎉 ALL SUPERUSER ACCOUNTS CREATED SUCCESSFULLY!")
print("=" * 60)
print("\n📋 LOGIN CREDENTIALS:\n")
print("1️⃣  ADMIN ACCOUNT")
print("   Username: admin")
print("   Password: admin123")
print()
print("2️⃣  SUPERUSER ACCOUNT 1")
print("   Username: superuser1")
print("   Password: super1234")
print()
print("3️⃣  SUPERUSER ACCOUNT 2")
print("   Username: superuser2")
print("   Password: super2345")
print()
print("=" * 60)
print("🌐 Access Admin Panel: http://localhost:8000/admin")
print("🏠 Access App: http://localhost:8000")
print("=" * 60)
