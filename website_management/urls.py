from django.conf.urls import url, patterns

from website_management import views


urlpatterns = patterns('',
    url(r'^$', views.website_dashboard, name='website_dashboard'),
    url(r'^webpage_detail/(?P<web_id>\d+)/$', views.webpage_detail, name='webpage_detail'),
    url(r'^homepage_detail/(?P<hp_id>\d+)/$', views.homepage_detail, name='homepage_detail'),
    url(r'^domain_detail/(?P<dom_id>\d+)/$', views.domain_detail, name='domain_detail'),
    url(r'^add_new_webpage/$', views.add_new_webpage, name='add_new_webpage'),
    url(r'^add_new_homepage/$', views.add_new_homepage, name='add_new_homepage'),
    url(r'^add_new_domain/$', views.add_new_domain, name='add_new_domain'),
    url(r'^view_all_webpage/$', views.view_all_webpage, name='view_all_webpage'),
    url(r'^view_all_homepage/$', views.view_all_homepage, name='view_all_homepage'),
    url(r'^view_all_domain/$', views.view_all_domain, name='view_all_domain'),
    url(r'^fetch_html_page/(?P<web_id>\d+)/$', views.fetch_html_page, name='fetch_html_page'),
    )
