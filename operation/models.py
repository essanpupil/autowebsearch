from django.db import models
from django.contrib.auth.models import User

class Operator(models.Model):
    'class model extension of default django User Model to add extra field (information)'
    user = models.OneToOneField(User)
    level = models.IntegerField()
    def __unicode__(self):
        return self.user.username

class Keyword(models.Model):
    'class model to save keyword used by application to query to search engine'
    user = models.ForeignKey(User)
    words = models.CharField(max_length=250, unique=True)
    search_area = models.CharField(max_length=10, default='webpage')
    create_time = models.DateField(auto_now=True)
    def __unicode__(self):
        return self.words

class Webpage(models.Model):
    'class model used to save all web page from search result'
    url = models.URLField(max_length=250, blank=False, unique=True)
    domain = models.CharField(max_length=250, blank=True)
    htmlPage = models.TextField(blank=True)
    textBody = models.TextField(blank=True)
    inspectStatus = models.BooleanField(default=False)
    scamStatus = models.BooleanField(default=False)
    reportStatus = models.BooleanField(default=False)
    accessStatus = models.BooleanField(default=False)
    def __unicode__(self):
        return self.url

class Tokens(models.Model):
    'class to saved tokens from websites'
    id = models.AutoField(primary_key=True)
    webpages = models.ManyToManyField(Webpage)
    sentence = models.TextField(max_length=512, unique=True)
    def __unicode__(self):
        return self.sentence

class UseToSearch(models.Model):
    'intermediete between Keyword and webpage'
    token = models.ForeignKey(Tokens, blank=True, null=True)
    keyword = models.ForeignKey(Keyword, blank=True, null=True)
    webpage = models.ForeignKey(Webpage)
    date = models.DateField(auto_now=True)

class Inspect(models.Model):
    'Intermediete class between Webpage and operator'
    user = models.ForeignKey(User)
    webpage = models.ForeignKey(Webpage)
    date = models.DateField(auto_now=True)

class CompareVia(models.Model):
    'intermediete between Webpage and Tokens'
    webpage = models.ForeignKey(Webpage)
    tokens = models.ForeignKey(Tokens)
    result = models.BooleanField(default=None) #comparison of webpage's tokens. the result is same or not for each token
    date = models.DateField(auto_now=True)