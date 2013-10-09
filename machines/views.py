from django.views.generic import ListView, DetailView
from machines.models import Machine, Tool, Driver, Axis


class MachineList(ListView):	
    def get_queryset(self):
    	return Machine.objects.filter(authorized_users=self.request.user)

class MachineDetail(DetailView):
	model = Machine

	def get_context_data(self, **kwargs):
		context = super(MachineDetail, self).get_context_data(**kwargs)
		#axis
		context['axis_list'] = Axis.objects.filter(machine = self.object)
		context['Axis_fields'] = Axis._meta.fields
		#tools
		context['tool_list'] = Tool.objects.filter(machine = self.object)
		context['Tool_fields'] = Tool._meta.fields
		return context

