from django.contrib import admin
from editor.models import Object, Job

def ObjectAdmin():
	search_feilds = ['name']
def JobAdmin():
	pass

admin.site.register(Object)
admin.site.register(Job)

