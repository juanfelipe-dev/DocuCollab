import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docucollab.settings')
django.setup()

from django.contrib.auth.models import User
from docs.models import UserRole

def create_admin():
    admin_username = 'admin'
    admin_password = 'admin123'
    admin_email = 'admin@example.com'
    if not User.objects.filter(username=admin_username).exists():
        u = User.objects.create_superuser(admin_username, admin_email, admin_password)
        UserRole.objects.get_or_create(user=u, role='admin')
        print(f'Created admin user: {admin_username}/{admin_password}')
    else:
        print('Admin user already exists')

def create_user1():
    username = 'user1'
    password = 'user1234'
    email = 'user1@example.com'
    if not User.objects.filter(username=username).exists():
        u = User.objects.create_user(username, email, password)
        UserRole.objects.get_or_create(user=u, role='user')
        print(f'Created user: {username}/{password}')
    else:
        print('User1 already exists')

if __name__ == "__main__":
    create_admin()
    create_user1()
