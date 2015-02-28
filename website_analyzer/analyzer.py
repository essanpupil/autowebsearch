from bs4 import BeautifulSoup

from website_management.models import Homepage, Webpage
from .models import ExtendHomepage, StringParameter, StringAnalysist


def string_analyst(hp_id):
    "function to do string analyst to homepage"
    hp = Homepage.objects.get(id=hp_id)
    exthp, created = ExtendHomepage.objects.get_or_create(homepage=hp)
    params = StringParameter.objects.all()
    for web in hp.webpage_set.all():
        for param in params:
            if param.name in web.extendwebpage.text_body:
                StringAnalysist.objects.create(webpage=web,
                                             parameter=param,
                                             find=True)
                if param.level == "1":
                    exthp.scam=True
                    exthp.save()
            else:
                StringAnalysist.objects.create(webpage=web,
                                             parameter=param,
                                             find=False)
