"""
Django management command to initialize the DocuCollab application.
Creates sample users with different roles for testing.
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from docs.models import UserRole


class Command(BaseCommand):
    help = 'Initialize DocuCollab application with sample users and roles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-users',
            action='store_true',
            help='Skip creating sample users',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting DocuCollab initialization...\n'))

        # Create sample users with different roles
        if not options['skip_users']:
            self.stdout.write('Creating sample users...')
            
            sample_users = [
                {
                    'username': 'admin',
                    'email': 'admin@docucollab.local',
                    'password': 'admin123',
                    'is_staff': True,
                    'is_superuser': True,
                    'role': 'admin',
                },
                {
                    'username': 'manager',
                    'email': 'manager@docucollab.local',
                    'password': 'manager123',
                    'is_staff': False,
                    'is_superuser': False,
                    'role': 'manager',
                },
                {
                    'username': 'user1',
                    'email': 'user1@docucollab.local',
                    'password': 'user123',
                    'is_staff': False,
                    'is_superuser': False,
                    'role': 'user',
                },
                {
                    'username': 'user2',
                    'email': 'user2@docucollab.local',
                    'password': 'user123',
                    'is_staff': False,
                    'is_superuser': False,
                    'role': 'user',
                },
            ]
            
            for user_data in sample_users:
                username = user_data['username']
                password = user_data.pop('password')
                role = user_data.pop('role')
                
                # Check if user already exists
                if User.objects.filter(username=username).exists():
                    self.stdout.write(
                        self.style.WARNING(f'  → User "{username}" already exists, skipping')
                    )
                    continue
                
                # Create user
                user = User.objects.create_user(**user_data, password=password)
                
                # Create or update user role
                if user.is_superuser:
                    user_role, created = UserRole.objects.get_or_create(
                        user=user,
                        defaults={'role': 'admin'}
                    )
                else:
                    user_role, created = UserRole.objects.get_or_create(
                        user=user,
                        defaults={'role': role}
                    )
                
                self.stdout.write(
                    self.style.SUCCESS(f'  ✓ Created user "{username}" with role "{role}"')
                )

        self.stdout.write(self.style.SUCCESS('\n✓ Initialization complete!'))
        self.stdout.write('\nSample Users Created:')
        self.stdout.write('  Admin:    admin / admin123')
        self.stdout.write('  Manager:  manager / manager123')
        self.stdout.write('  User 1:   user1 / user123')
        self.stdout.write('  User 2:   user2 / user123')
        self.stdout.write('\nAccess the application at: http://localhost:8000')
        self.stdout.write('Admin panel at: http://localhost:8000/admin\n')
