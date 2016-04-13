"filter module for views in website_analyzer app."
import django_filters

from website_management.models import Domain, Website


class ExtendDomainFilter(django_filters.FilterSet):
    "filter based on ExtendDomain model"
    name = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = Domain
        fields = ['name', 'extenddomain__free', 'extenddomain__whitelist']


class ExtendHomepageFilter(django_filters.FilterSet):
    "filter based on ExtendHomepage model"
    name = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = Website
        fields = ['name',
                  'extendwebsite__scam',
                  'extendwebsite__whitelist']
