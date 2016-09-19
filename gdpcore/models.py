from django.db import models

from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
# from polikif import models as polikif_models


class Cycle(models.Model):
	autor = models.ForeignKey(User)
	text = models.CharField(max_length = 1000)
	creation_date = models.DateTimeField()
	proposition_initiale = models.IntegerField(default=0)
	nb = models.IntegerField(default=1)
	last_prop_date = models.DateTimeField()

	def __str__(self):
		return str(self.id)

class Proposition(models.Model):
	NATURE_PROP_CHOICE = (
		('Diagnostic','Diagnostic'),
		('Action','Action'),
		('Reference','Reference'),
		('YT','Youtube'),
		('SY','Syllogisme')
	)
	autor = models.ForeignKey(User)
	text = models.CharField(max_length = 3000)
	nature = models.CharField(max_length = 30, choices = NATURE_PROP_CHOICE, default = 'Diagnostic')
	cycle = models.ForeignKey(Cycle)
	
	tags = models.CharField(max_length = 3000, default = '')
	simil = models.FloatField(default=0)
	creation_date = models.DateTimeField()
	modification_date = models.DateTimeField()
	trafic = models.IntegerField(default=0)

	demande_precision = models.BooleanField(default=False)
	demande_supplement = models.BooleanField(default=False)
	demande_attention = models.BooleanField(default=False)
	
	ytid = models.CharField(max_length = 30, default = '')
	videoBeginning = models.IntegerField(default=0)
	videoEnd = models.IntegerField(default=0)
	
	def __str__(self):
		return str(self.id)

class LinkType(models.Model):
	type = models.CharField(max_length = 100)
	text = models.CharField(max_length = 100, default = '')
	logic = models.CharField(max_length = 100)
	sens = models.BooleanField()
	inverse = models.CharField(max_length = 100)
	strokeColor = models.CharField(max_length = 100)
	strokeWidth =  models.IntegerField()
	arrows = models.IntegerField()
	
	def __str__(self):
		return str(self.id)
			
class Link(models.Model):
	NATURE_LINK_CHOICE = (
		('Exemple','Exemple'),
		('Donc','Donc'),
		('Concurrence','Concurrence'),
		('Syl','Syl'),
		('E','Exemple'),
		('D','Donc'),
		('C','Concurrence')
	)
	
	STATUS_CHOICE = (
		('A','Active'),
		('I','Inactive'),
		('P','Pending'),
	)
	autor = models.ForeignKey(User)
	creation_date = models.DateTimeField()
	modification_date = models.DateTimeField()
	nature = models.CharField(max_length = 30, choices = NATURE_LINK_CHOICE, default = 'Donc')
	type = models.ForeignKey(LinkType)
	status = models.CharField(max_length = 30, choices = STATUS_CHOICE, default = 'A')
	cycle = models.ForeignKey(Cycle)
	trafic = models.IntegerField(default=0)
	
	left_prop = models.ForeignKey(Proposition, related_name='%(class)s_left_prop')
	#If that's a syllogisme :
	second_left_prop = models.ForeignKey(Proposition, related_name='%(class)s_second_left_prop', blank=True, null=True)
	
	right_prop = models.ForeignKey(Proposition, related_name='%(class)s_right_prop')	
	junction = models.CharField(max_length = 30, default = '')
	
	def __str__(self):
		return str(self.id)
		
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
	
	def __str__(self):
		return str(self.id)

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
		('DS','Demande de source'),
		('DV','Demande de validation de lien'),
		
	)
	autor = models.ForeignKey(User)
	proposition = models.ForeignKey(Proposition)
	nature = models.CharField(max_length = 30, choices = NATURE_NOTIFICATION_CHOICE, default = 'Reponse')
	creation_date = models.DateTimeField()
	modification_date = models.DateTimeField()
	viewed = models.BooleanField()
	def __str__(self):
		return str(self.id)
	
class Implication(models.Model):
	autor = models.ForeignKey(User)
	proposition = models.ForeignKey(Proposition)
	link = models.ForeignKey(Link)
	creation_date = models.DateTimeField()
	def __str__(self):
		return str(self.id)

class Graph(models.Model):
	autor = models.ForeignKey(User)
	graphstring = models.CharField(max_length = 10000, default = '')
	title = models.CharField(max_length = 300)
	originx = models.IntegerField(default=0)
	originy = models.IntegerField(default=0)
	creation_date = models.DateTimeField()
	propNumber = models.IntegerField(default=0)	
	parti = models.ForeignKey('polikif.Parti', default = 1)
	
	history = HistoricalRecords()
	
	
	def __str__(self):
		return str(self.id)
		
class Elemgraph(models.Model):
	graph = models.ForeignKey(Graph)
	x = models.IntegerField(default=0)
	y = models.IntegerField(default=0)
	proposition = models.ForeignKey(Proposition)
	displayed = models.BooleanField()
	def __str__(self):
		return str(self.id)	

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	picture = models.ImageField(upload_to='pictures')
	
class CommentGraph(models.Model):
	graph = models.ForeignKey(Graph)
	author = models.ForeignKey(User)
	text = models.CharField(max_length = 1000)
	creation_date = models.DateTimeField()
	
	proposition = models.ForeignKey(Proposition, blank=True, null=True)
	link = models.ForeignKey(Link, blank=True, null=True)
	comment = models.ForeignKey('self', blank=True, null=True)
	
	visibility = models.BooleanField(default = True)
		
class Show(models.Model):
	author = models.ForeignKey(User)
	title = models.CharField(max_length = 100)
	description = models.CharField(max_length = 1000, default ='')
	audio = models.FileField(upload_to="audio", blank=True, null=True)

	def __str__(self):
		return str(self.id)	
	
class ShowPart(models.Model):
	show = models.ForeignKey(Show)
	order = models.IntegerField()
	text = models.CharField(max_length = 3000, blank=True, null=True)
	proposition = models.ForeignKey(Proposition, blank=True, null=True)
	x = models.IntegerField(default = 0)
	y = models.IntegerField(default = 0)
	link = models.ForeignKey(Link, blank=True, null=True)
	duration = models.FloatField(default = 3)
	audio = models.FileField(upload_to='audioex', blank=True, null=True)
	
	def __str__(self):
		return str(self.id)		