from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.admin_dashboard, name='admin_dashboard'),
    # client url section
    url(r'^add-client/$',
        views.add_client, name='add_client'),
    url(r'^view-client/$',
        views.view_client, name='view_client'),
    url(r'^edit-client/(?P<pk>\d+)/$',
        views.EditClient.as_view(), name='edit_client'),
    url(r'^delete-client/(?P<client_id>\d+)/$',
        views.delete_client, name='delete_client'),
    url(r'^delete-client-process/$',
        views.delete_client_process, name='delete_client_process'),
    url(r'^detail-client/(?P<client_id>\d+)/$',
        views.detail_client, name='detail_client'),
    url(r'^add-homepage/(?P<client_id>\d+)/$',
        views.add_homepage, name='add_homepage'),
    url(r'^delete-homepage/(?P<pk>\d+)/$',
        views.WebsiteDelete.as_view(), name='delete_homepage'),
    url(r'^delete-homepage-success/$',
        views.delete_homepage_success,
        name='delete_client_website_success'),

    # operator url section
    url(r'^add-operator/$',
        views.add_operator, name='add_operator'),
    url(r'^view-operator/$',
        views.view_operator, name='view_operator'),
    url(r'^edit-operator/(?P<operator_id>\d+)/$',
        views.edit_operator, name='edit_operator'),
    url(r'^delete-operator/(?P<operator_id>\d+)/$',
        views.delete_operator, name='delete_operator'),

    # user url section
    url(r'^add-user/$', views.add_user, name='add_user'),
    url(r'^view-user/$',
        views.view_user, name='view_user'),
    url(r'^edit-user/(?P<user_id>\d+)/$',
        views.edit_user, name='edit_user'),
    url(r'^delete-user/(?P<user_id>\d+)/$',
        views.delete_user, name='delete_user'),

    # event url section
    url(r'^add-event/$', views.add_event, name='add_event'),
    url(r'^view-event/$',
        views.view_event, name='view_event'),
    url(r'^edit-event/(?P<event_id>\d+)/$',
        views.edit_event, name='edit_event'),
    url(r'^delete-event/(?P<event_id>\d+)/$',
        views.delete_event, name='delete_event'),

    ]

