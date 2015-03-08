from django.conf.urls import url, patterns

from website_analyzer import views


urlpatterns = patterns('',
                       url(r'^$', views.analyst_dashboard,
                           name='analyst_dashboard'),
                       url(r'^analyze_website/(?P<hp_id>\d+)/$',
                           views.analyze_website, name='analyze_website'),
                       url(r'^start_analyze/(?P<hp_id>\d+)/$',
                           views.start_analyze, name='start_analyze'),
                       url(r'^display_pages/$', views.display_pages,
                           name='display_pages'),
                       url(r'^display_analyst/$', views.display_analyst,
                           name='display_analyst'),
                       url(r'^edit_analyst/$', views.edit_analyst,
                           name='edit_analyst'),
                       url(r'^view_tokens/$', views.view_tokens,
                           name='view_tokens'),
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
                      )
