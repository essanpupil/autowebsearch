from django.db import models


class Domain(models.Model):
    "Store webpages domain"
    name = models.CharField(unique=True, max_length=75)
    def __unicode__(self):
        return self.name

class Homepage(models.Model):
    "Store homepages of webpages"
    name = models.CharField(max_length=100, unique=True)
    domain = models.ForeignKey(Domain)
    def __unicode__(self):
        return self.name

class Webpage(models.Model):
    "Store webpages"
    url = models.URLField(max_length=250, blank=True, unique=True)
    homepage = models.ForeignKey(Homepage, blank=True, null=True)
    html_page = models.TextField(blank=True, null=True)
    def __unicode__(self):
        return self.url
