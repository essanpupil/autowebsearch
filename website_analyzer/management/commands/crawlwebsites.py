from django.core.management.base import BaseCommand, CommandError

from website_analyzer.models import ExtendHomepage
from website_analyzer.analyzer_lib import crawl_website


class Command(BaseCommand):
    args = 'Arguments are not needed'
    help = "Search webpages with saved queries"
    
    def handle(self, *args, **options):
        ext_obj = ExtendHomepage.objects.exclude(whitelist=True)
        ext_hp = ext_obj.order_by('full_crawled')[0]
        crawl_website(ext_hp.homepage)
