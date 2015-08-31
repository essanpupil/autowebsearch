import django_filters

from .models import Webpage


class WebpageFilter(django_filters.FilterSet):
    "filtering Webpage model"
    url = django_filters.CharFilter(label='Alamat halaman web', lookup_type='icontains')
    class Meta:
        model = Webpage
        fields = ['url']
