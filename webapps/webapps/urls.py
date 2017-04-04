"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from socialnetwork import views,urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('socialnetwork.urls')),
    # url(r'^$', views.index, name = 'index'),
    # url(r'^login/$', views.user_login, name='login'),
    # url(r'^homepage/$', views.go_home, name = 'homepage'),
    # url(r'^register/$', views.user_register, name='register'),
    # url(r'^homepage/(?P<pk>[A-Za-z0-9]+)/$', views.view_profile, name='profile'),
    # url(r'^editprofile/$', views.edit_profile, name='edit'),
    # url(r'^postpage/$', views.post_message, name='post'),
    # url(r'^logout/$', views.logout, name='logout'),
    # url(r'^accounts/login/$',views.user_login),
    # url(r'^accounts/logout/$',views.logout),
    # url(r'^viewyourprofile/$', views.view_yourprofile, name='vewyourprofile'),
    # url(r'^picture/(?P<id>[A-Za-z0-9]+)/$', views.getphoto, name='picture'),
    # url(r'^follow/(?P<id>[A-Za-z0-9]+)/$',views.follow_user,name = 'follow'),
    # url(r'^unfollow/(?P<id>[A-Za-z0-9]+)/$',views.unfollow,name = 'unfollow'),
    # url(r'picture/(?P<id>[A-Za-z0-9]+)/$', views.getphoto),

    # url(r'add_comment$', views.add_comment),
    # url(r'get_list_json$', views.get_list_json),
    # url(r'get_list_xml$', views.get_list_xml),
    # url(r'get_list_xml_template$', views.get_list_xml_template),

    # url(r'^confirm_registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$',
    #     views.confirm_registration, name='confirm'),
    
]
