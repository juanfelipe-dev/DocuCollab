import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docucollab.settings')
django.setup()

from django.contrib.auth.models import User
from docs.models import UserRole

for username, pwd in [('regular1', 'user1234'), ('regular2', 'user2345'), ('regular3', 'user3456')]:
    u, created = User.objects.get_or_create(username=username)
    if created:
        u.set_password(pwd)
        u.save()
        UserRole.objects.create(user=u, role='user')
        print(f'Created regular user {username}/{pwd}')
    else:
        print(f'{username} already exists')
