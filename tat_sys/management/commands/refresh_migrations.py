from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.apps import apps

class Command(BaseCommand):
    help = 'Deletes all table data and re-applies migrations.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Resetting database...'))

        for app in apps.get_app_configs():
            try:
                call_command('migrate', app.label, 'zero', interactive=False)
                self.stdout.write(self.style.SUCCESS(f'Successfully rolled back {app.label}'))
            except CommandError as e:
                self.stdout.write(self.style.ERROR(f'Error rolling back {app.label}: {e}'))

        call_command('migrate', interactive=False)
        self.stdout.write(self.style.SUCCESS('Successfully re-applied migrations.'))
