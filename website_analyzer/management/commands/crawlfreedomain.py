from django.core.management.base import BaseCommand, CommandError

from website_analyzer.models import ExtendDomain
from website_analyzer.analyzer_lib import crawl_website


class Command(BaseCommand):
    args = 'Arguments are not needed'
    help = "Search webpages with saved queries"
    
    def handle(self, *args, **options):
        ext_doms = ExtendDomain.objects.filter(free=True)
        ext_dom = ext_doms.order_by('times_crawled')
        if len(ext_dom) > 0:
            homepages = ext_dom[0].domain.homepage_set.all()
            for homepage in homepages:
                crawl_website(homepage)
            ext_dom[0].times_crawled += 1
            ext_dom[0].save()
        else:
            print "No free domain"
