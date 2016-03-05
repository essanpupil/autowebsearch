from django.core.management.base import BaseCommand

from website_analyzer.models import ExtendHomepage
from website_analyzer.analyzer_lib import string_analyst


class Command(BaseCommand):
    args = 'Arguments is not needed'
    help = 'Executing string analyst to homepage'

    def handle(self, *args, **options):
        ext_hps = ExtendHomepage.objects.exclude(whitelist=True)
        ext_hps2 = ext_hps.filter(full_crawled__gt=0)
        ext_hps3 = ext_hps2.order_by('times_analyzed')
        string_analyst(ext_hps3[0].homepage.id)
