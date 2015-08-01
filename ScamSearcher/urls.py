from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import login, logout, welcome

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', welcome, name='welcome'),
                       url(r'^login$', login, name='login'),
                       url(r'^logout$', logout, name='logout'),
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
