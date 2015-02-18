from django.db import models

from website_management.models import Webpage, Homepage, Domain


class ExtendDomain(models.Model):
    "extend model Domain to add more information"
    domain = models.OneToOneField(Domain)

    # True if the domain is freely available (blogspot, wordpress, etc).
    free = models.NullBooleanField(null=True, blank=True)


class ExtendHomepage(models.Model):
    "extending homepage model to add more field"
    homepage = models.OneToOneField(Homepage)
    
    # True if the website is a scam, False if not, None if not sure
    scam = models.NullBooleanField(blank=True, null=True)

    # True if he webpage is already inspected, False if not yet inspected.
    inspected = models.BooleanField(default=False)

    # True if the website is already inspected, False if not yet or no need to.
    reported =  models.NullBooleanField(blank=True, null=True)

    # True if the website response is 200 (accessible), else it is False
    access =  models.BooleanField(default=True)

    # True if the web should bewhitelist, False if should not, None pending
    whitelist =  models.NullBooleanField(blank=True, null=True)

    #method to validate form data input when editing homepage value
    def clean(self):
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

    #method to correctly save whitelist value when the homepage scam is True
    def save(self, *args, **kwargs):
        if self.scam == False:
            self.whitelist = True
        elif self.scam == True:
            self.whitelist = False
        else:
            super(Extend, self).save(*args, **kwargs)


class ExtendWebpage(models.Model):
    " extending the Webpage model for additional info require for analisis"
    webpage = models.OneToOneField(Webpage)


class Token(models.Model):
    """ store tokens used in webpages. tokens used to create keyword search
    and analisis parameter """
    id = models.AutoField(primary_key=True)
    webpage = models.ManyToManyField(Webpage)
    name = models.CharField(max_length=20, unique=True)
    def __unicode__(self):
        return self.name


class sequence(models.Model):
    "store sequence token, use as parameter for analyzing website"
    id = models.AutoField(primary_key=True)
    token = models.ForeignKey(Token)

    # webpages using this sequence
    webpage = models.ForeignKey(Webpage)

    # token's number on a certain sequence.
    number = models.IntegerField()

    # short description about the sequence.
    description = models.CharField(max_length=255, unique=True)
    def __unicode__(self):
        return self.description


class searching(models.Model):
    'information on each searching activity'
    id = models.AutoField(primary_key=True)
    keyword = models.CharField(max_length=255)
    webpages = models.ForeignKey(Webpage)
    date = models.DateField(auto_now=True)
    def __unicode__(self):
        return self.date
