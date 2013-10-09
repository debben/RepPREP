from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template


# Uncomment the next two lines to enable the admin:
from django.contrib import admin, auth

from RepPREP import views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'index', views.index, name="index"),
	url(r'^objects/', include('editor.urls', namespace='object')),
	url(r'^machines/', include('machines.urls', namespace='machines')),
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^admin/', include(admin.site.urls)),
)
