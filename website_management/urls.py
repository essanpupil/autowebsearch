from django.conf.urls import url, patterns

from website_management import views


urlpatterns = patterns('',
    url(r'^$', views.website_dashboard, name='website_dashboard'),
    url(r'^webpage_detail/(?P<web_id>\d+)/$', views.webpage_detail,
                                            name='webpage_detail'),
    url(r'^homepage_detail/(?P<hp_id>\d+)/$', views.homepage_detail,
                                            name='homepage_detail'),
    url(r'^domain_detail/(?P<dom_id>\d+)/$', views.domain_detail,
                                            name='domain_detail'),
    url(r'^add_new_webpage/$', views.add_new_webpage,
                                            name='add_new_webpage'),
    url(r'^view_all_webpages/$', views.view_all_webpages,
                                            name='view_all_webpages'),
    url(r'^view_all_homepages/$', views.view_all_homepages,
                                            name='view_all_homepages'),
    url(r'^view_all_domains/$', views.view_all_domains,
                                            name='view_all_domains'),
    url(r'^fetch_html_page/(?P<web_id>\d+)/$', views.fetch_html_page,
                                            name='fetch_html_page'),
    )
