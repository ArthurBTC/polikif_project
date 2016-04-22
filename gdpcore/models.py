from django.db import models

from django.contrib.auth.models import User


class Cycle(models.Model):
	autor = models.ForeignKey(User)
	text = models.CharField(max_length = 1000)
	creation_date = models.DateTimeField()
	proposition_initiale = models.IntegerField(default=0)
	nb = models.IntegerField(default=1)
	last_prop_date = models.DateTimeField()

#	def __str__(self):
#		return self.id


class Proposition(models.Model):
	NATURE_PROP_CHOICE = (
		('Diagnostic','Diagnostic'),
		('Action','Action'),
		('Reference','Reference'),
	)
	autor = models.ForeignKey(User)
	text = models.CharField(max_length = 3000)
	
	tags = models.CharField(max_length = 3000)
	simil = models.FloatField(default=0)
	
	creation_date = models.DateTimeField()
	modification_date = models.DateTimeField()
	cycle = models.ForeignKey(Cycle)
	nature = models.CharField(max_length = 30, choices = NATURE_PROP_CHOICE, default = 'Diagnostic')
	trafic = models.IntegerField(default=0)

	demande_precision = models.BooleanField()
	demande_supplement = models.BooleanField()
	demande_attention = models.BooleanField()
	
#	def __str__(self):
#		return self.text

		
class Link(models.Model):
	NATURE_LINK_CHOICE = (
		('Exemple','Exemple'),
		('Donc','Donc'),
		('Concurrence','Concurrence'),
		('Syl','Syl'),

	)
	autor = models.ForeignKey(User)
	creation_date = models.DateTimeField()
	modification_date = models.DateTimeField()
	nature = models.CharField(max_length = 30, choices = NATURE_LINK_CHOICE, default = 'Donc')
	cycle = models.ForeignKey(Cycle)
	trafic = models.IntegerField(default=0)
	
	left_prop = models.ForeignKey(Proposition, related_name='%(class)s_left_prop')
	#If that's a syllogisme :
	second_left_prop = models.ForeignKey(Proposition, related_name='%(class)s_second_left_prop', blank=True, null=True)
	
	right_prop = models.ForeignKey(Proposition, related_name='%(class)s_right_prop')
	
	
	
	junction = models.CharField(max_length = 30)
	
#	def __str__(self):
#		return self.id
		
class Comment(models.Model):
	NATURE_COMMENT_CHOICE = (
		('Text','Text'),
		('Precision','Precision'),
		('Supplement','Supplement'),
		('Attention','Attention'),
		
		('MP','Modification de proposition'),
		('CA',"Changement d'avis"),
		('NP','Nouvelle proposition'),
		('TX','Texte'),
		('DP','Demande de précision'),
		('DS','Demande de supplément')
		
		
	)
	autor = models.ForeignKey(User)
	nature = models.CharField(max_length = 30, choices = NATURE_COMMENT_CHOICE, default = 'Text')
	text = models.CharField(max_length = 1000)
	creation_date = models.DateTimeField()
	proposition = models.ForeignKey(Proposition)
	
#	def __str__(self):
#		return self.id

	
class Notification(models.Model):
	NATURE_NOTIFICATION_CHOICE = (
		('Reponse','Reponse'),
		('Demande','Demande'),
		("Demande d'attention","Demande d'attention"),
		('Demande de précision','Demande de précision'),
		('Demande de source','Demande de source'),
		
		
		('NL','Nouveau lien'),
		('MP','Modification de proposition'),
		('CA',"Changement d'avis"),
		('SP','Suppression de proposition'),
		('CL','Critique de lien'),
		('NC','Nouveau commentaire'),
		('DA',"Demande d'attention"),
		('DP','Demande de précision'),
		('DS','Demande de source')
		
	)
	autor = models.ForeignKey(User)
	proposition = models.ForeignKey(Proposition)
	nature = models.CharField(max_length = 30, choices = NATURE_NOTIFICATION_CHOICE, default = 'Reponse')
	creation_date = models.DateTimeField()
	modification_date = models.DateTimeField()
	viewed = models.BooleanField()
	
#	def __str__(self):
#		return self.id
	
	
class Implication(models.Model):
	autor = models.ForeignKey(User)
	proposition = models.ForeignKey(Proposition)
	link = models.ForeignKey(Link)
	creation_date = models.DateTimeField()


	
	

