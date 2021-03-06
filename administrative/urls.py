"""urls module for adminstrative app."""
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    url(r'^$', views.admin_dashboard, name='admin_dashboard'),
    # client url section
    url(r'^add-client/$',
        views.add_client, name='add_client'),
    url(r'^view-client/$',
        views.view_client, name='view_client'),
    url(r'^edit-client/(?P<pk>\d+)/$',
        login_required(views.EditClient.as_view()), name='edit_client'),
    url(r'^delete-client/(?P<client_id>\d+)/$',
        views.delete_client, name='delete_client'),
    url(r'^delete-client-process/$',
        views.delete_client_process, name='delete_client_process'),
    url(r'^detail-client/(?P<client_id>\d+)/$',
        views.detail_client, name='detail_client'),
    url(r'^add-homepage/(?P<client_id>\d+)/$',
        views.add_homepage, name='add_homepage'),
    url(r'^delete-homepage/(?P<pk>\d+)/$',
        login_required(views.WebsiteDelete.as_view()),
        name='delete_homepage'),
    url(r'^delete-homepage-success/$',
        views.delete_homepage_success,
        name='delete_client_website_success'),
    url(r'^view-event/(?P<client_id>\d+)/$',
        views.view_event, name='view_event'),
    url(r'^add-event/(?P<client_id>\d+)/$',
        views.add_event, name='add_event'),
    url(r'^edit-event/(?P<pk>\d+)/$',
        login_required(views.EditEvent.as_view()),
        name='edit_event'),
    url(r'^delete-event/(?P<event_id>\d+)/$',
        views.delete_event, name='delete_event'),
    url(r'^delete-event-process/$',
        views.delete_event_process, name='delete_event_process'),
    url(r'^detail-event/(?P<event_id>\d+)/$',
        views.detail_event, name='detail_event'),
    url(r'^view-client-keyword/(?P<client_id>\d+)/$',
        views.view_client_keyword, name='view_client_keyword'),
    url(r'^add-client-keyword/(?P<client_id>\d+)/$',
        views.add_client_keyword, name='add_client_keyword'),
    url(r'^view-client-sequence/(?P<client_id>\d+)/$',
        views.view_client_sequence, name='view_client_sequence'),
    url(r'^add-client-sequence/(?P<client_id>\d+)/$',
        views.add_client_sequence, name='add_client_sequence'),

    # operator url section
    url(r'^add-operator/(?P<client_id>\d+)/$',
        views.add_operator, name='add_operator'),
    url(r'^view-operator/(?P<client_id>\d+)/$',
        views.view_operator, name='view_operator'),
    url(r'^edit-operator/(?P<operator_id>\d+)/$',
        views.edit_operator, name='edit_operator'),
    url(r'^edit-operator-process/$',
        views.edit_operator_process, name='edit_operator_process'),
    url(r'^delete-operator/(?P<operator_id>\d+)/$',
        views.delete_operator, name='delete_operator'),
    url(r'^delete-operator-process/$',
        views.delete_operator_process, name='delete_operator_process'),

    # user url section
    url(r'^add-user/$', views.add_user, name='add_user'),
    url(r'^view-user/$',
        views.view_user, name='view_user'),
    url(r'^edit-user/(?P<pk>\d+)/$',
        login_required(views.EditUser.as_view()),
        name='edit_user'),
    url(r'^delete-user/(?P<pk>\d+)/$',
        login_required(views.DeleteUser.as_view()),
        name='delete_user'),

    # event url section
    url(r'^view-all-event/$',
        views.view_all_event, name='view_all_event'),
    url(r'^view-sent-mail/$',
        views.view_sent_mail,
        name='view_sent_mail'),
    ]
