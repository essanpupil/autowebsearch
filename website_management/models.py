"""models module for website_management app."""
from django.db import models


class Domain(models.Model):
    """Store webpages domain"""
    name = models.CharField(unique=True, max_length=75)
    date_added = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Homepage(models.Model):
    """Store homepages of webpages"""
    name = models.CharField(max_length=100, unique=True)
    domain = models.ForeignKey(Domain, blank=True, null=True)
    date_added = models.DateField(auto_now=True)
    crawl_completed = models.BooleanField(default=False)
    times_analyzed = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Webpage(models.Model):
    """Store webpages"""
    url = models.URLField(max_length=255, unique=True)
    full_url = models.TextField(blank=True, default="")
    homepage = models.ForeignKey(Homepage, blank=True, null=True)
    html_page = models.TextField(blank=True)
    date_added = models.DateField(auto_now=True)
    last_response = models.CharField(max_length=3, blank=True)
    last_response_check = models.DateField(blank=True, null=True)
    redirect_url = models.URLField(blank=True)
    times_crawled = models.IntegerField(default=0)

    def __str__(self):
        return self.url
