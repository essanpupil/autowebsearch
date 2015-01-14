'''
Created on Jan 12, 2015

@author: pupil
'''
from django.conf.urls import patterns, url
from operation import views

urlpatterns = patterns('',
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^webpages/$', views.webpages, name='webpages'),
    url(r'^webpages/view_all/$', views.view_all_webpages, name='view_all_webpages'),
    url(r'^webpages/add_new/$', views.add_new_webpage, name='add_new_webpage'),
    url(r'^webpages/process_add_new/$', views.process_add_new_webpage, name='process_add_new_webpage'),
    url(r'^tokens/$', views.tokens, name='tokens'),
    url(r'^tokens/view_all/$', views.view_all_tokens, name='view_all_tokens'),
    url(r'^tokens/add_new/$', views.add_new_token, name='add_new_token'),
    url(r'^tokens/process_add_new/$', views.process_add_new_token, name='process_add_new_token'),
    url(r'^manual_search/(?P<keyword_id>\d+)/$', views.manual_search, name='manual_search'),
    url(r'^manual_search/result/$', views.manual_search_result, name='manual_search_result'),
    url(r'^get_web_source/(?P<web_id>\d+)/$', views.get_web_source, name='get_web_source'),
    url(r'^web_detail/(?P<web_id>\d+)/$', views.web_detail, name='web_detail'),
    url(r'^settings/$', views.settings, name='settings'),
)
