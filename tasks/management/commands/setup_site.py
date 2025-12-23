from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = 'Sets up the site with the correct domain and name'

    def handle(self, *args, **options):
        # Get the current site (which is created by default)
        site = Site.objects.get_current()
        
        # Update the site domain and name
        site.domain = '127.0.0.1:8000'
        site.name = 'Local Development'
        site.save()
        
        self.stdout.write(self.style.SUCCESS('Successfully updated site settings'))
        self.stdout.write(f'Site domain: {site.domain}')
        self.stdout.write(f'Site name: {site.name}')
