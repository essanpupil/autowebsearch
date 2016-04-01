"""urls module for website_analyzer app."""
from django.conf.urls import url

from website_analyzer import views


urlpatterns = [
    url(r'^$', views.analyst_dashboard,
        name='analyst_dashboard'),
    url(r'^analyze_website/(?P<hp_id>\d+)/$',
        views.analyze_website, name='analyze_website'),
    url(r'^start_analyze/(?P<hp_id>\d+)/$',
        views.start_analyze, name='start_analyze'),
    url(r'^extract_links/(?P<web_id>\d+)/$',
        views.extract_links, name='extract_links'),
    url(r'^add_scam_website/$', views.add_scam_website,
        name='add_scam_website'),
    url(r'^view_websites/$', views.view_websites,
        name='view_websites'),
    url(r'^view_sequence/$', views.view_sequence,
        name='view_sequence'),
    url(r'^add_sequence/$', views.add_sequence,
        name='add_sequence'),
    url(r'^crawl_website/(?P<homepage_id>\d+)/$',
        views.crawl_homepage,
        name='crawl_website'),
    url(r'^start_sequence_analysist/(?P<homepage_id>\d+)$',
        views.start_sequence_analysist,
        name='start_sequence_analysist'),
    url(r'^view_analyst_result$', views.view_analyst_result,
        name='view_analyst_result'),
    url(r'^view_analyst_domains/$',
        views.view_analyst_domains,
        name='view_analyst_domains'),
    url(r'^edit_analyst_domain/(?P<dom_id>\d+)/$',
        views.edit_analyst_domain,
        name='edit_analyst_domain'),
    url(r'^detail_analyst_domain/(?P<dom_id>\d+)/$',
        views.detail_analyst_domain,
        name='detail_analyst_domain'),
    ]
