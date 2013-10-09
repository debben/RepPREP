from django.db import models
from machines.models import Machine
from django.contrib.auth.models import User

class Object(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    model_url = models.URLField()
    gcode = models.TextField()
    owner = models.ForeignKey(User)
    #TODO: Put a link to a profile tag for gcode


    def __unicode__(self):
        return self.name
   
class Job(models.Model):
	#guid for the job
    machine = models.ForeignKey(Machine)
    user = models.ForeignKey(User)
    started_on = models.DateTimeField()
    finished_on = models.DateTimeField()
    eta = models.IntegerField() #estimated runtime in ms
    #option fields (support, color, material)
    
    
