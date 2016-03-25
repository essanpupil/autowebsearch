"""models module for website_analyzer app."""
from django.db import models
from django.core.exceptions import ValidationError

from website_management.models import Webpage, Homepage, Domain


class ExtendDomain(models.Model):
    """extend model Domain to add more information"""
    WHITELIST_CHOICES = ((True, 'YES'),
                         (False, 'NO'),
                         (None, 'UNKNOWN'))
    domain = models.OneToOneField(Domain)
    # True if the web should be whitelist, False if should not, None pending
    whitelist = models.NullBooleanField(max_length=7,
                                        choices=WHITELIST_CHOICES,
                                        blank=True,
                                        null=True)
    # True if the domain is freely available (blogspot, wordpress, etc).
    free = models.NullBooleanField(null=True, blank=True)
    times_crawled = models.IntegerField(default=0)


class ExtendHomepage(models.Model):
    """extending homepage model to add more field"""
    SCAM_CHOICES = ((True, 'YES'),
                    (False, 'NO'),
                    (None, 'UNKNOWN'))
    WHITELIST_CHOICES = ((True, 'YES'),
                         (False, 'NO'),
                         (None, 'UNKNOWN'))
    homepage = models.OneToOneField(Homepage)
    full_crawled = models.IntegerField(default=0)
    times_analyzed = models.IntegerField(default=0)
    # value: 'yes', 'no', 'unknown'
    scam = models.NullBooleanField(max_length=7, choices=SCAM_CHOICES,
                                   blank=True, null=True)
    # True if he webpage is already inspected, False if not yet inspected.
    inspected = models.BooleanField(default=False)
    # 'unreport', 'reported', 'postpone'
    reported = models.BooleanField(default=False)
    # True if the website response is 200 (accessible), else it is False
    access = models.BooleanField(default=True)
    # True if the web should be whitelist, False if should not, None pending
    whitelist = models.NullBooleanField(max_length=7,
                                        choices=WHITELIST_CHOICES,
                                        blank=True,
                                        null=True)
    # method to validate form data input when editing homepage value
    def clean(self):
        "custom clean to make sure scam status whitelist not conflict"
        if self.scam and self.whitelist:
            raise ValidationError("""
                                  Scam and whitelist status can not have
                                  the same value unless the value is None
                                  """)
        elif self.scam is False and self.whitelist is False:
            raise ValidationError("""
                                  Scam and whitelist status can not have
                                  the same value unless the value is None
                                  """)

    # method to correctly save whitelist value when the homepage scam is True
    def save(self, *args, **kwargs):
        "override save() to make sure scam & wwhitelist not conflict"
        if self.scam is False:
            self.whitelist = True
            super(ExtendHomepage, self).save(*args, **kwargs)
        elif self.scam is True:
            self.whitelist = False
            super(ExtendHomepage, self).save(*args, **kwargs)
        else:
            super(ExtendHomepage, self).save(*args, **kwargs)


class ExtendWebpage(models.Model):
    """ extending the Webpage model for additional info require for analisis"""
    webpage = models.OneToOneField(Webpage)
    text_body = models.TextField(blank=True)


class Token(models.Model):
    """ store tokens used in webpages. tokens used to create keyword search
    and analisis parameter """
    id = models.AutoField(primary_key=True)  # lint:ok
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):  # lint:ok
        return self.name


class Pieces(models.Model):
    """Token sequence number on webpage"""
    webpage = models.ForeignKey(Webpage)
    token = models.ForeignKey(Token)
    number = models.IntegerField()


class SequenceDescription(models.Model):
    """store the description of each sequence"""
    name = models.CharField(max_length=255, unique=True)


class StringParameter(models.Model):
    """Store string parameter to be search during analysist"""
    sentence = models.CharField(max_length=255, unique=True)
    definitive = models.BooleanField(default=False)
    date_added = models.DateField(auto_now=True)

    def __str__(self):  # lint:ok
        return self.sentence


class StringAnalysist(models.Model):
    """Store string parameter analysist result of webpage's"""
    webpage = models.ForeignKey(Webpage)
    parameter = models.ForeignKey(StringParameter)
    time = models.DateTimeField(auto_now=True)
    find = models.BooleanField(default=False)


class Sequence(models.Model):
    """store sequence token, use as parameter for analyzing website"""
    id = models.AutoField(primary_key=True)  # lint:ok
    token = models.ForeignKey(Token)
    # webpages using this sequence
    webpage = models.ForeignKey(Webpage, blank=True, null=True)
    # token's number on a certain sequence.
    number = models.IntegerField()
    # short description about the sequence.
    description = models.ForeignKey(SequenceDescription)

    def __str__(self):  # lint:ok
        return self.description


class Searching(models.Model):
    """information on each searching activity"""
    id = models.AutoField(primary_key=True)  # lint:ok
    keyword = models.CharField(max_length=255)
    webpages = models.ForeignKey(Webpage)
    date = models.DateField(auto_now=True)

    def __str__(self):  # lint:ok
        return self.date
