"""helper module for administrative app."""
from website_management.management_lib import add_url_to_webpage
from website_management.models import Webpage

from administrative.models import Client, Website


def save_client(name=None, email=None, phone=None, address=None):
    """Save submited client to database."""
    Client.objects.create(name=name, email=email, phone=phone, address=address)


def save_client_homepage(client, url, event=None):
    """Save homepage for this specific client."""
    add_url_to_webpage(url)
    webpage = Webpage.objects.get(url=url)
    Website.objects.create(
        homepage=webpage.homepage, client=client, event=event)
