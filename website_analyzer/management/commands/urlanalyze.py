from django.core.management.base import BaseCommand, CommandError

from website_analyzer.models import ExtendHomepage, StringParameter
from website_analyzer.analyzer_lib import string_analyst, crawl_website


class Command(BaseCommand):
    args = 'Arguments is not needed'
    help = 'Executing string analyst to homepage'

    def handle(self, *args, **options):
        str_prm = StringParameter.objects.filter(target_analyze="url")    
        str_prm2 = str_prm.order_by('times_used')[0]
        str_prm2.times_used += 1
        str_prm2.save(update_fields=['times_used'])
        ext_hps = ExtendHomepage.objects.exclude(whitelist=True)
        ext_hps2 = ext_hps.filter(homepage__name__icontains=str_prm2.sentence)
        ext_hps3 = ext_hps2.order_by('times_analyzed')
        crawl_website(ext_hps3[0].homepage)
        string_analyst(ext_hps3[0].homepage.id)
