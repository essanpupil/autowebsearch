from django.db import models
from django.contrib.auth.models import User

class Operator(models.Model):
    'class model extension of default django User Model to add extra field (information)'
    user = models.OneToOneField(User)
    username = models.CharField(max_length=250)

class Keyword(models.Model):
    'class model to save keyword used by application to query to search engine'
    words = models.CharField(max_length=250, unique=True)
    #operator = models.ForeignKey(Operator)
    createTime = models.DateField(auto_now=True)

class SearchEngine(models.Model):
    'class model to save search engine used to search url/keyword in internet'
    name = models.CharField(max_length=250)
    domain = models.CharField(max_length=250)
    queryParameter = models.CharField(max_length=250)
    pageParameter = models.CharField(max_length=250)
    finalPageText = models.CharField(max_length=250)

class QueriedTo(models.Model):
    'intermediet class between Operator and SearchEngine'
    operator = models.ForeignKey(Operator)
    searchengine = models.ForeignKey(SearchEngine)
    time = models.DateField(auto_now=True)

class Webpage(models.Model):
    'class model used to save all web page from search result'
    url = models.URLField(max_length=250, blank=False)
    domain = models.CharField(max_length=250, blank=True)
    htmlPage = models.TextField(blank=True)
    textBody = models.TextField(blank=True)
    inspectStatus = models.BooleanField(default=False)
    scamStatus = models.BooleanField(default=False)
    reportStatus = models.BooleanField(default=False)
    accessStatus = models.BooleanField(default=False)

class Inspect(models.Model):
    'Intermediete class between Webpage and operator'
    inspectTime = models.DateTimeField()
