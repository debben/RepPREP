from django.conf.urls import patterns, url
from editor.views import ObjectList, ObjectEditor

urlpatterns = patterns('',
    url(r'^$', ObjectList.as_view()),
    url(r'^(?P<pk>\d+)/$', ObjectEditor.as_view()),    
)
