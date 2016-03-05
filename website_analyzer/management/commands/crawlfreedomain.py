from django.core.management.base import BaseCommand

from website_analyzer.models import ExtendDomain
from website_analyzer.analyzer_lib import crawl_website


class Command(BaseCommand):
    args = 'Arguments are not needed'
    help = "Search webpages with saved queries"
    
    def handle(self, *args, **options):
        ext_doms = ExtendDomain.objects.only('times_crawled',
                                             'domain',
                                             'free').filter(free=True)
        ext_dom = ext_doms.order_by('times_crawled')
        if len(ext_dom) > 0:
            ext_dom[0].times_crawled += 1
            ext_dom[0].save(update_fields=['times_crawled'])
            homepages = ext_dom[0].domain.homepage_set.all()[:1]
            for homepage in homepages:
                crawl_website(homepage)
        else:
            print("No free domain")
