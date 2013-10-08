from django.db import models
from django.contrib.auth.models import User

X = 'x'
Y = 'y'
Z = 'z'
A = 'a'
B = 'b'
C = 'c'
D = 'd'
AXIS = (
	(X, 'x axis'),
	(Y, 'y axis'),
	(Z, 'z axis'),
	(A, 'a axis'),
	(B, 'b axis'),	
	(C, 'c axis'),
	(D, 'd axis'),
	)

class Machine(models.Model):
	name = models.CharField(max_length=50)
	warmup = models.TextField(blank=True,
							  null=True)
	cooldown = models.TextField(blank=True,null=True)
	geometry = models.CharField(max_length=20)
	#owner = models.ForeignKey(User)	
	authorized_users = models.ManyToManyField(User)
	def __unicode__(self):
		return self.name

class Axis(models.Model):
	label = models.CharField(max_length=1,
								choices=AXIS,
								verbose_name='Axis')
	length = models.IntegerField()
	maxfeedrate = models.IntegerField(blank=True,
									  null=True,
									  verbose_name='Max Feed Rate')
	homingfeedrate = models.IntegerField(blank=True
										,null=True,
										verbose_name='Homing Feed Rate')
	stepspermm = models.FloatField(blank=True
									,null=True,
									verbose_name= 'Steps Per mm')
	scale = models.FloatField(blank=True,
								null=True)
	endstops = models.CharField(max_length=20)
	machine = models.ForeignKey(Machine)


	def __unicode__(self):
		return self.label

class Driver(models.Model):
	portname = models.CharField(max_length=100)
	rate = models.IntegerField(default=115200)
	machine = models.ForeignKey(Machine)
	parity = models.IntegerField(default=8)
	databits = models.IntegerField(default = 1,blank=True,null=True)
	stopbits = models.IntegerField(blank=True,null=True)
	deubuglevel = models.IntegerField(blank=True,null=True)


class Tool(models.Model):	
	name = models.CharField(max_length=50)
	model = models.CharField(max_length=50)
	diameter = models.FloatField()
	stepper_axis = models.CharField(max_length=1,
									choices=AXIS,
									default=A)
	index = models.IntegerField(default=0)
	type = models.CharField(max_length=50)
	motor = models.BooleanField(default=True)
	fan = models.BooleanField(default=False)
	heatedplatform = models.BooleanField(default=False)
	motor_steps = models.IntegerField(blank=True,null=True)
	default_rpm = models.IntegerField(blank=True,null=True)
	heater = models.BooleanField(default=True)
	machine = models.ForeignKey(Machine)
	material = models.CharField(max_length=20, blank=True,null=True)
	valve = models.BooleanField(default=False)

	def __unicode__(self):
		return self.name	






