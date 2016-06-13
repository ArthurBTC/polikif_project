from django.db import models

from django.contrib.auth.models import User
from gdpcore import models as gdpcore_models


class Parti(models.Model):
	name = models.CharField(max_length = 1000)
	description = models.CharField(max_length = 1000)
	creation_date = models.DateTimeField()
	
	def __str__(self):
		return str(self.id)
	
class Cellule(models.Model):
	parti = models.ForeignKey(Parti)
	name = models.CharField(max_length = 1000)
	description = models.CharField(max_length = 1000)
	creation_date = models.DateTimeField()


class Adhesion_parti(models.Model):
	ROLE_CHOICE = (
		('PP','Président parti'),
		('DTK','Directeur Think Tank'),
		('M','Membre'),
	)
	
	STATUS_CHOICE = (
		('A','Active'),
		('I','Inactive'),
		('P','Pending'),
	)

	user = models.ForeignKey(User)
	parti = models.ForeignKey(Parti)
	role = models.CharField(max_length = 30, choices = ROLE_CHOICE, default = 'M')
	status = models.CharField(max_length = 30, choices = STATUS_CHOICE, default = 'A')
	creation_date = models.DateTimeField()
	
		
	
class Adhesion_cellule(models.Model):
	ROLE_CHOICE = (
		('DC','Directeur Cellule'),
		('M','Membre'),
	)
	
	STATUS_CHOICE = (
		('A','Active'),
		('I','Inactive'),
		('P','Pending'),
	)

	user = models.ForeignKey(User)
	cellule = models.ForeignKey(Cellule)
	role = models.CharField(max_length = 30, choices = ROLE_CHOICE, default = 'M')
	status = models.CharField(max_length = 30, choices = STATUS_CHOICE, default = 'A')
	creation_date = models.DateTimeField()

class Selection(models.Model):
	TYPE_CHOICE = (
		('O','Officielle'),
		('A','Acceptée'),
		('R','Rejetée'),
	)
	
	STATUS_CHOICE = (
		('A','Active'),
		('I','Inactive'),
		('P','Pending'),
	)

	proposition = models.ForeignKey(gdpcore_models.Proposition)
	user = models.ForeignKey(User)
	parti = models.ForeignKey(Parti)
	
	category = models.CharField(max_length = 100)
	
	type = models.CharField(max_length = 30, choices = TYPE_CHOICE, default = 'M')
	status = models.CharField(max_length = 30, choices = STATUS_CHOICE, default = 'A')
	creation_date = models.DateTimeField()
	
# class UserProfile(models.Model)
	# user = models.OneToOneField(User, on_delete=models.CASCADE)
	# parti = models.ForeignKey(Parti, blank=True, null=True)
	# cellules = models.ManyToManyField(Cellule, , blank=True, null=True)
	
