from django.core.management.base import BaseCommand, CommandError
from shortener.models import CirrURL

class Command(BaseCommand):
    help = 'Refresh all CirrURL shortcodes'

    def add_arguments(self, parser):
        parser.add_argument('--items', type=int)

        # parser.add_argument('--items', type=int)

    def handle(self, *args, **options):
        return CirrURL.objects.refresh_shortcode(items=options['items'])