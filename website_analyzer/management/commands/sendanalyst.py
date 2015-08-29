from django.core.management.base import BaseCommand, CommandError

from website_analyzer.models import Homepage, StringAnalysist
from website_analyzer.analyzer_lib import string_analyst, crawl_website,\
                                          send_email_website_analyze
from administrative.models import ClientSequence


class Command(BaseCommand):
    args = 'Arguments is not needed'
    help = 'Executing string analyst to homepage'

    def handle(self, *args, **options):
        sa_web = StringAnalysist.objects.all()
        for sa in sa_web:
            if sa.webpage.homepage.extendhomepage.sent_mail == True:
                continue
            else:
                client_recipients = []
                cs = ClientSequence.objects.filter(
                            string_parameter=sa.parameter)
                for item2 in cs:
                    client_recipients.append(item2.client)
                operator_recipients = []
                for client in client_recipients:
                    for operator in client.operator_set.all():
                        operator_recipients.append(operator)
                send_email_website_analyze(
                        sa.webpage.homepage, operator_recipients)
