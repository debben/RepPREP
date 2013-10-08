from django.http import HttpResponse
from polls.models import Poll
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404


def index(request):	
	return render(request, 'index.html', {'testName': 'this is the name'})

def dashboard(request):
	return null

def login(request):
	return render(request, 'login.html', {'test' : 'test'})