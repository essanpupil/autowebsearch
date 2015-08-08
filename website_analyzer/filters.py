import django_filters

from .models import ExtendHomepage, ExtendDomain
from website_management.models import Domain


class ExtendDomainFilter(django_filters.FilterSet):
    class Meta:
        model = Domain
        fields = ['extenddomain__free', 'extenddomain__whitelist']
