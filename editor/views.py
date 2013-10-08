from django.http import HttpResponse
from polls.models import Poll
from django.template import RequestContext
from pyjade.ext.django.loader import Loader
from django.shortcuts import render, get_object_or_404


def about(request):		
	return render(request, 'about.jade', {'testName': 'this is the name'})
