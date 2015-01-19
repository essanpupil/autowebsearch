'''
Created on Jan 12, 2015

@author: pupil
'''
from django.conf.urls import patterns, url
from operation import views

urlpatterns = patterns('',
    url(r'^process_login/$', views.process_login, name='process_login'),
    url(r'^process_logout/$', views.process_logout, name='process_logout'),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),

    url(r'^keywords/$', views.keywords, name='keywords'),
    url(r'^keywords/add_new/$', views.add_new_keyword, name='add_new_keyword'),
    url(r'^keywords/process_add_new/$', views.process_add_new_keyword, name='process_add_new_keyword'),
    #url(r'^keywords/view_detail/(?P<keyword_id>\d+)/$', views.view_keyword_detail, name='view_keyword_detail'),
    #url(r'^keywords/process_edit_keyword/$', views.process_eit_keyword, name='process_edit_keyword'),

    #url(r'^admin/$', views.admin, name='admin'),
    #url(r'^admin/view_all_operator/$', views.view_all_operator, name='view_all_operator'),
    #url(r'^admin/view_operator_detail/(?P<operator_id>\d+)/$', views.view_admin_detail, name='view_admin_detail'),
    #url(r'^admin/process_edit_operator/$', views.process_edit_operator, name='process_edit_operator'),

    url(r'^operator/$', views.operator_detail, name='operator'),
    url(r'^operator/change_password_operator/$', views.change_password_operator, name='change_password_operator'),
    url(r'^operator/process_change_password_operator/$', views.process_change_password_operator, name='process_change_password_operator'),
    url(r'^operation/change_password_result/(?P<message>\D+)/$', views.change_password_result, name='change_password_result'),
    #url(r'^operator/process_edit_my_detail/$', views.process_edit_my_detail, name='process_edit_my_detail'),
    #url(r'^operator/my_log/$', views.my_log, name='my_log'),

    url(r'^webpages/$', views.webpages, name='webpages'),
    #url(r'^webpages/compare_tokens/(?P<web_id>\d+)/$', views.compare_tokens, name='compare-tokens'),
    #url(r'^webpages/inspect_web/(?P<web_id>\d+)/$', views.inspect_web, name='inspect_web'),
    url(r'^webpages/fetch_html_source/(?P<web_id>\d+)/$', views.fetch_html_source, name='fetch_html_source'),
    url(r'^webpages/view_web_detail/(?P<web_id>\d+)/$', views.view_web_detail, name='view_web_detail'),
    url(r'^webpages/full_webpage_tokens/(?P<web_id>\d+)/$', views.full_webpage_tokens, name='full_webpage_tokens'),
    url(r'^webpages/report_website/(?P<web_id>\d+)/$', views.report_website, name='report_website'),
    url(r'^webpages/process_saving_inspection/$', views.process_saving_inspection, name='process_saving_inspection'),
    url(r'^webpages/add_new_webpage/$', views.add_new_webpage, name='add_new_webpage'),
    url(r'^webpages/process_add_new/$', views.process_add_new_webpage, name='process_add_new_webpage'),
    url(r'^webpages/manual_search/(?P<keyword_id>\d+)/$', views.manual_search_webpages, name='manual_search_webpages'),
    url(r'^webpages/manual_search_result/$', views.manual_search_result, name='manual_search_result'),

    url(r'^tokens/$', views.tokens, name='tokens'),
    url(r'^tokens/view_all/$', views.view_all_tokens, name='view_all_tokens'),
)
