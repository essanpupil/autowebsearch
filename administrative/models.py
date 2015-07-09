from django.db import models

from website_management.models import Homepage

class Client(models.Model):
    "Place to save everybody that use this application service"
    name = models.CharField(max_length=255, null=False, blank=False,)
    email = models.EmailField(null=False, blank=False)
    phone = models.CharField(max_length=15, null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    date_start = models.DateField(auto_now_add=True)
    date_end = models.DateField(null=True, blank=True)
    def __unicode__(self):
        return self.name

class Event(models.Model):
    "Place to save events held by clients"
    client = models.ForeignKey(Client, default=None)
    name = models.CharField(max_length=255, null=False, blank=False)
    time_start = models.DateField(auto_now_add=True)
    time_end = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Operator(models.Model):
    "This is Client's employee"
    name = models.CharField(max_length=100, null=False, blank=False)
    client = models.ForeignKey(Client)
    event = models.ManyToManyField(Event, blank=True)
    email = models.EmailField(null=False, blank=False)
    date_start = models.DateField(auto_now_add=True)
    date_end = models.DateField(null=True, blank=True)
    def __unicode__(self):
       return self.name


class Website(models.Model):
    "Save websites used by event and clients"
    homepage = models.OneToOneField(Homepage)
    client = models.ForeignKey(Client)
    event = models.ForeignKey(Event, null=True, blank=True)
    def __unicode__(self):
        return self.homepage.name
