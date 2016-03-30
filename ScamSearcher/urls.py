"""ROOT_URLCONF for ScamSearcher project."""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from ScamSearcher.views import login, logout, welcome, user_profile, \
                               password_changed
from website_management.views import website_dashboard


urlpatterns = (
    url(r'^$', website_dashboard, name='welcome'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login$', login, name='login'),
    url(r'^logout$', logout, name='logout'),
    url(r'^login/', auth_views.login, name='login'),
    url(r'^logout/', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^password_change/',
        auth_views.password_change,
        {'post_change_redirect': 'password_changed'},
        name='password_change'),
    url(r'^password_changed/$',
        password_changed,
        name='password_changed'),
    url(r'^$', welcome, name='welcome'),
    url(r'^profile/$', user_profile, name='user_profile'),

    url(r'^website_management/',
        include('website_management.urls',
                namespace='website_management',
                app_name='website_management')),
    url(r'^website_analyzer/',
        include('website_analyzer.urls',
                namespace='website_analyzer',
                app_name='website_analyzer')),
    url(r'^administrative/',
        include('administrative.urls',
                namespace='administrative',
                app_name='administrative')),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
