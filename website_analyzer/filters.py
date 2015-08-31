import django_filters

from website_management.models import Domain, Homepage


class ExtendDomainFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type='icontains')
    class Meta:
        model = Domain
        fields = ['name','extenddomain__free', 'extenddomain__whitelist']


class ExtendHomepageFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label='Nama website', lookup_type='icontains')
    class Meta:
        model = Homepage
        fields = ['name',
                  'extendhomepage__scam',
                  'extendhomepage__use_as_parameter',
                  'extendhomepage__whitelist']
