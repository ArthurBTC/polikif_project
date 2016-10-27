from django.db import models
import django.contrib.auth.models
from gdpcore import models as gdpcoreModels


# Create your models here.
class Organisation(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return str(self.id)


class Speaker(models.Model):
    name = models.CharField(max_length=300)
    account = models.ForeignKey(django.contrib.auth.models.User, blank=True, null=True)
    description = models.CharField(max_length=1000)
    picture = models.ImageField(upload_to='speakers')
    status = models.CharField(max_length=10, default = 'default')

    def __str__(self):
        return str(self.name)


class Event(models.Model):
    organisation = models.ForeignKey(Organisation)
    speakers = models.ManyToManyField(Speaker, blank=True, null=True)
    graph = models.ForeignKey(gdpcoreModels.Graph, blank=True, null=True)
    show = models.ForeignKey(gdpcoreModels.Show, related_name="show", blank=True, null=True)
    show2 = models.ForeignKey(gdpcoreModels.Show, related_name="show2", blank=True, null=True)

    name = models.CharField(max_length=1000, default = 'default')
    description = models.CharField(max_length=2000, default = 'default')
    date = models.DateTimeField()
    place = models.CharField(max_length=1000)
    
    inscriptionurl = models.CharField(max_length=1000, default='default')

    STATUS_CHOICE = (
        ('0', 'à venir'),
        ('1', 'passé')
    )

    status = models.CharField(max_length=30, choices=STATUS_CHOICE, default='0')
    
    displayphoto = models.BooleanField(default = False)
    displaydescription = models.BooleanField(default = False)
    displayfacilitation = models.BooleanField(default = False)
    displayintervenant = models.BooleanField(default = False)
    displayanimation = models.BooleanField(default = False)
    displayinscription = models.BooleanField(default = False)
    

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
    # record = models.ForeignKey(Record)
    proposition = models.ManyToManyField(gdpcoreModels.Proposition)
    event = models.ForeignKey(Event)
    speaker = models.ForeignKey(Speaker)
    order = models.IntegerField(default=0)
    text = models.CharField(max_length=1000)
    status = models.IntegerField(default = 0)

    def __str__(self):
        return str(self.text)


class Question(models.Model):
    text = models.CharField(max_length=1000)
    firstname = models.CharField(max_length=100, default='', blank=True, null=True)
    lastname = models.CharField(max_length=100, default='', blank=True, null=True)
    email = models.CharField(max_length=100, default='', blank=True, null=True)
    phone = models.CharField(max_length=30, default='', blank=True, null=True)
    showpart = models.ManyToManyField(gdpcoreModels.ShowPart)
    event = models.ForeignKey(Event, default = 1)
    time = models.DateTimeField()

    def __str__(self):
        return str(self.text)
        
class Converter(models.Model):
    html = models.CharField(max_length= 100000)
    event = models.ForeignKey(Event, blank=True, null=True)
    
    def __str__(self):
        return str(self.id)
        
class Conseil(models.Model):
    conseil = models.FileField(upload_to='conseils')
    event = models.ForeignKey(Event)
    