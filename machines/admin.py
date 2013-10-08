from django.contrib import admin
from machines.models import Machine, Axis, Tool, Driver

def MachineAdmin():
	search_feilds = ['name']
def AxisAdmin():
	pass
def ToolAdmin():
	pass
def DriverAdmin():
	pass

admin.site.register(Machine)#, MachineAdmin)
admin.site.register(Axis)#, AxisAdmin)
admin.site.register(Tool)#, ToolAdmin)
admin.site.register(Driver)#, DriverAdmin)
