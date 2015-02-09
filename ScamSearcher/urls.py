from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    #url(r'^interface/', include('operation.urls'))
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^website_management/', include('website_management.urls', namespace='website_management', app_name='website_management')),
)
