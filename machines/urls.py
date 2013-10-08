from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from machines.models import Machine
from machines.views import MachineList, MachineDetail

urlpatterns = patterns('',
    url(r'^$', MachineList.as_view()),
    url(r'^(?P<pk>\d+)/$', MachineDetail.as_view()),    

)