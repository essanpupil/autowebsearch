from django.db import models


class Domain(models.Model):
    """Store webpages domain"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=75)
    date_added = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.name


class Homepage(models.Model):
    """Store homepages of webpages"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    domain = models.ForeignKey(Domain, blank=True, null=True)
    date_added = models.DateField(auto_now=True)
    crawl_completed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Webpage(models.Model):
    """Store webpages"""
    id = models.AutoField(primary_key=True)
    url = models.URLField(max_length=250, unique=True)
    homepage = models.ForeignKey(Homepage, blank=True, null=True)
    html_page = models.TextField(blank=True, null=True)
    date_added = models.DateField(auto_now=True)
    last_response = models.CharField(max_length=3, blank=True, null=True)
    last_response_check = models.DateField(blank=True, null=True)
    redirect_url = models.URLField(null=True, blank=True)
    times_crawled = models.IntegerField(default=0)

    def __unicode__(self):
        return self.url


class Query(models.Model):
    "Store keyword used to search in google"
    keywords = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.keywords


class Search(models.Model):
    "Save search result"
    query = models.ForeignKey(Query, blank=False, null=False)
    webpage = models.ForeignKey(Webpage, blank=False, null=False)
    search_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.search_time
