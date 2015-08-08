import django_filters

from website_management.models import Domain, Homepage


class ExtendDomainFilter(django_filters.FilterSet):
    class Meta:
        model = Domain
        fields = ['name','extenddomain__free', 'extenddomain__whitelist']


class ExtendHomepageFilter(django_filters.FilterSet):
    class Meta:
        model = Homepage
        fields = ['name',
                  'extendhomepage__scam',
                  'extendhomepage__whitelist']
