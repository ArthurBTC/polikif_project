from django.db import models
from gdpcore import models as gdpcore_models
# Create your models here.

class Organisation(models.Model):
	name = models.CharField(max_length = 300)

	def __str__(self):
		return str(self.id)
		
class Speaker(models.Model):
	name = models.CharField(max_length = 300)
	description = models.CharField(max_length = 1000)

	def __str__(self):
		return str(self.id)
		
class Event(models.Model):
	
	organisation = models.ForeignKey(Organisation)
	speakers = models.ManyToManyField(Speaker)
	graph = models.ForeignKey(gdpcore_models.Graph)
	show = models.ForeignKey(gdpcore_models.Show)
	
	name = models.CharField(max_length = 1000)
	description = models.CharField(max_length = 2000)
	date = models.DateTimeField()
	place = models.CharField(max_length = 1000)

	STATUS_CHOICE = (
		('0','à venir'),
		('1','passé')
	)

	status = models.CharField(max_length = 30, choices = STATUS_CHOICE, default = '0')
		
	def __str__(self):
		return str(self.id)
		
class Record(models.Model):
	event = models.ForeignKey(Event)
	speaker = models.ForeignKey(Speaker)
	record = models.FileField(upload_to='records')

	def __str__(self):
		return str(self.record)
		
		
class Photo(models.Model):
	event = models.ForeignKey(Event)
	picture = models.ImageField(upload_to='pictures')

	def __str__(self):
		return str(self.id)		

class Sentence(models.Model):
#	record = models.ForeignKey(Record)
	proposition = models.ForeignKey(gdpcore_models.Proposition)
	event = models.ForeignKey(Event)
	speaker = models.ForeignKey(Speaker)
	order = models.IntegerField(default = 0)
	text = models.CharField(max_length = 1000)

	def __str__(self):
		return str(self.text)	
	
class Question(models.Model):
	text = models.CharField(max_length = 1000)
	firstname = models.CharField(max_length = 100, default='')
	lastname = models.CharField(max_length = 100, default='')
	email = models.CharField(max_length = 100, default='')
	phone = models.CharField(max_length = 30, default='')
	show = models.ForeignKey(gdpcore_models.Show)
	
	def __str__(self):
		return str(self.text)	