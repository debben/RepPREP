from django.http import HttpResponse
from polls.models import Poll
from django.template import RequestContext
from pyjade.ext.django.loader import Loader
from django.shortcuts import render, get_object_or_404

from django.views.generic import ListView, DetailView
from editor.models import Object, Job

class ObjectList(ListView):
	model = Object
	template_name = "objects/object_list.html"

class ObjectEditor(DetailView):
	model = Object
	template_name = "editor/editor.html"

	def get_context_data(self, **kwargs):
		context = super(ObjectEditor, self).get_context_data(**kwargs)
		return context


