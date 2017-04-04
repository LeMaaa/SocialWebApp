from django.conf.urls import url,include
from django.contrib import admin
from socialnetwork import views as socialnetwork_views


urlpatterns = [
    url(r'^$', socialnetwork_views.index, name = 'index'),
    url(r'^login/$', socialnetwork_views.user_login, name='login'),
    url(r'^homepage/$', socialnetwork_views.go_home, name = 'homepage'),
    url(r'^register/$', socialnetwork_views.user_register, name='register'),
    url(r'^homepage/(?P<pk>[A-Za-z0-9]+)/$', socialnetwork_views.view_profile, name='profile'),
    url(r'^editprofile/$', socialnetwork_views.edit_profile, name='edit'),
    url(r'^postpage/$', socialnetwork_views.post_message, name='post'),
    url(r'^logout/$', socialnetwork_views.logout, name='logout'),
    url(r'^accounts/login/$',socialnetwork_views.user_login),
    url(r'^accounts/logout/$',socialnetwork_views.logout),
    url(r'^viewyourprofile/$', socialnetwork_views.view_yourprofile, name='vewyourprofile'),
    url(r'^picture/(?P<id>[A-Za-z0-9]+)/$', socialnetwork_views.getphoto, name='picture'),
    url(r'^follow/(?P<id>[A-Za-z0-9]+)/$',socialnetwork_views.follow_user,name = 'follow'),
    url(r'^unfollow/(?P<id>[A-Za-z0-9]+)/$',socialnetwork_views.unfollow,name = 'unfollow'),
    url(r'picture/(?P<id>[A-Za-z0-9]+)/$', socialnetwork_views.getphoto),

    url(r'add_comment$', socialnetwork_views.add_comment),
    url(r'get_list_json$', socialnetwork_views.get_list_json),
    url(r'get_list_xml$', socialnetwork_views.get_list_xml),
    url(r'get_list_xml_template$', socialnetwork_views.get_list_xml_template),

    url(r'^confirm_registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$',
        socialnetwork_views.confirm_registration, name='confirm'),
    ]