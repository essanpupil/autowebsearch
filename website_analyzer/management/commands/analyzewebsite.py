from django.core.management.base import BaseCommand, CommandError

from website_analyzer.models import Homepage
from website_analyzer.analyzer_lib import string_analyst, crawl_website


class Command(BaseCommand):
    args = 'Arguments is not needed'
    help = 'Executing string analyst to homepage'

    def handle(self, *args, **options):
        homepages = Homepage.objects.exclude(
                extendhomepage__whitelist=True,
                extendhomepage__use_as_parameter=True).order_by(
                    'extendhomepage__times_string_analyzed').only('id')
        string_analyst(homepages[0].id)
