from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^interface/', include('operation.urls'))
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^', include('django.contrib.auth.urls')),
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

# handler404 = '
