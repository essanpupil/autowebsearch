"custom admin command to analyze based on webpage's url"
from django.core.management.base import BaseCommand

from website_analyzer.models import ExtendHomepage, StringParameter
from website_analyzer.analyzer_lib import string_analyst, crawl_website
from website_management.models import Homepage


class Command(BaseCommand):
    args = 'Arguments is not needed'
    help = 'Executing string analyst to homepage'

    def handle(self, *args, **options):
        str_prm = StringParameter.objects.filter(target_analyze="url")
        str_prm2 = str_prm.order_by('times_used')[0]
        str_prm2.times_used += 1
        str_prm2.save(update_fields=['times_used'])
        hps = Homepage.objects.filter(
            name__icontains=str_prm2.sentence).order_by('times_analyzed')
        for x in range(0, hps.count()):
            ext_hp, _ = ExtendHomepage.objects.get_or_create(homepage=hps[x])
            if ext_hp.whitelist is not True:
                hps[x].times_analyzed += 1
                hps[x].save(update_fields=['times_analyzed'])
                ext_hp = ExtendHomepage.objects.get_or_create(homepage=hps[x])
                crawl_website(hps[x])
                string_analyst(hps[x].id)
                break
            else:
                continue
