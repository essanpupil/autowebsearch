from .models import Client


def save_client(name=None, email=None, phone=None, address=None):
    """
    Save submited client to database
    """
    Client.objects.create(name=name, email=email, phone=phone,
                          address=address)
