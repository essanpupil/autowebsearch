from django.core.management.base import BaseCommand, CommandError

from website_analyzer.models import ExtendHomepage
from website_analyzer.analyzer_lib import string_analyst, crawl_website


class Command(BaseCommand):
    args = 'Arguments is not needed'
    help = 'Executing string analyst to homepage'

    def handle(self, *args, **options):
        ext_hps = ExtendHomepage.objects.exclude(whitelist=True)
        ext_hps = ext_hps.filter(full_crawled__gt=0)
        ext_hps = ext_hps.order_by('times_analyzed')
        string_analyst(ext_hps[0].homepage.id)
