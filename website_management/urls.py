"""urls module for website_management app."""
from django.conf.urls import url

from website_management import views


urlpatterns = [
    url(r'^$', views.website_dashboard,
        name='website_dashboard'),
    url(r'^homepage_detail/(?P<hp_id>\d+)/$',
        views.homepage_detail, name='homepage_detail'),
    url(r'^view_all_homepages/$',
        views.view_all_homepages, name='view_all_homepages'),
    url(r'^view_all_keywords/$',
        views.view_all_keywords, name='view_all_keywords'),
]
