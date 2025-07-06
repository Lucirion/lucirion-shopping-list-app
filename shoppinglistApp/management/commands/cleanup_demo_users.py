from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Deletes all demo users created via demo-login'

    def handle(self, *args, **kwargs):
        demo_users = User.objects.filter(username__startswith='demo_')
        count = demo_users.count()
        demo_users.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} demo users.'))
