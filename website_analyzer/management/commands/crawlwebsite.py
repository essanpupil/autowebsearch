from django.core.management.base import BaseCommand, CommandError

from website_analyzer.models import ExtendHomepage
from website_analyzer.analyzer_lib import crawl_website
from website_management.models import Homepage


class Command(BaseCommand):
    help = "Crawl website from available webpages"

    def add_arguments(self, parser):
        parser.add_argument('website_name', nargs='+', type=str)
    
    def handle(self, *args, **options):
        for website_name in options['website_name']:
            try:
                website = Homepage.objects.get(name=website_name)
            except Homepage.DoesNotExist:
                raise CommandError("Website '%s' doesn't exist" % website_name)
            ext_hp, created = ExtendHomepage.objects.get_or_create(
                    homepage = website)
            ext_hp.full_crawled += 1
            ext_hp.save(update_fields=['full_crawled'])
            crawl_website(website)
