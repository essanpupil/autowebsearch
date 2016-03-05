from django.core.management.base import BaseCommand

from website_analyzer.models import ExtendHomepage, ExtendDomain


class Command(BaseCommand):
    args = 'Arguments is not needed'
    help = 'Executing string analyst to homepage'

    def handle(self, *args, **options):
        ext_doms = ExtendDomain.objects.filter(whitelist=True)
        for ext_dom in ext_doms:
            if ext_dom.whitelist:
                ext_hps = ExtendHomepage.objects.filter(
                    homepage__domain=ext_dom.domain)
                for ext_hp in ext_hps:
                    ext_hp.whitelist = ext_dom.whitelist
                    ext_hp.save()
