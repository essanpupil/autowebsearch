from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

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
                       url(r'^edit_analyst/(?P<homepage_id>\d+)/$',
                           views.edit_analyst, name='edit_analyst'),
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
                       url(r'^view_clients_analyst/$',
                           views.view_client_analyst,
                           name='view_client_analyst'),
                       url(r'^detail_client_analyst/(?P<client_id>\d+)/$',
                           views.detail_client_analyst,
                           name='detail_client_analyst'),
                        url(r'^edit-sequence/(?P<pk>\d+)/$',
                            login_required(views.SequenceUpdate.as_view()),
                            name='edit_sequence'),
                        url(r'^report-website/(?P<hp_id>\d+)/$',
                            views.report_website,
                            name='report_website'),
                        url(r'^send-email-notification/(?P<hp_id>\d+)/$',
                            views.send_email_notification,
                            name='send_email_notification'),
                       url(r'^analyze_webpage/(?P<webpage_id>\d+)/$',
                           views.analyze_webpage, name='analyze_webpage'),
                       url(r'^get_word_token_website/(?P<homepage_id>\d+)/$',
                            views.get_word_token_website,
                            name='get_word_token_website'),
                       url(r'^get_word_token_webpage/(?P<webpage_id>\d+)/$',
                            views.get_word_token_webpage,
                            name='get_word_token_webpage'),
                       url(r'^start_ratio_analysist/(?P<homepage_id>\d+)$',
                           views.start_ratio_analysist,
                           name='start_ratio_analysist'),
                       )
