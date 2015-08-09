from django.db import models
from django.contrib.auth.models import User

from website_management.models import Homepage, Query
from website_analyzer.models import StringParameter

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
    user = models.OneToOneField(User)
    client = models.ForeignKey(Client)
    event = models.ManyToManyField(Event, blank=True)
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


class ClientKeyword(models.Model):
    "save keyword for specific client"
    query = models.OneToOneField(Query)
    client = models.ForeignKey(Client)
    
    def __unicode__(self):
        return self.query.keywords


class ClientSequence(models.Model):
    "save keyword for specific client"
    string_parameter = models.OneToOneField(StringParameter)
    client = models.ForeignKey(Client)
    event = models.ForeignKey(Event, null=True, blank=True)
    
    def __unicode__(self):
        return self.string_parameter.sentence


class SentEmail(models.Model):
    "Stored sent email to client or staff"
    recipient = models.ForeignKey(User)
    homepage = models.ForeignKey(Homepage)
    sent_time = models.DateTimeField(auto_now_add=True)
