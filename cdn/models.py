from django.db import models
import django.contrib.auth.models


class Member(models.Model):
    idmeetup = models.IntegerField()
    name = models.CharField(max_length = 1000)
    role = models.CharField(max_length = 1000)
    status = models.CharField(max_length = 1000)
    presenceCount = models.IntegerField(default = 0)
    organisationCount = models.IntegerField(default = 0)
    photo = models.CharField(max_length = 1000, blank=True, null=True)

    def __str__(self):
        return str(self.name)

class Place(models.Model):
    idmeetup = models.IntegerField()
    name = models.CharField(max_length = 1000, default= 'default')
    adress = models.CharField(max_length = 1000, default= 'default')
    
    def __str__(self):
        return str(self.name)
        
class Event(models.Model):
    idmeetup = models.IntegerField()
    name = models.CharField(max_length = 1000, default= 'default')
    status = models.CharField(max_length = 1000, default = 'default')
    organisator = models.ForeignKey(Member)
    time = models.DateTimeField()
    place = models.ForeignKey(Place)
    
    def __str__(self):
        return str(self.name)   

        
class Presence(models.Model):
    member = models.ForeignKey(Member)
    event = models.ForeignKey(Event)
    guest = models.BooleanField(default = False)
    status = models.CharField(max_length = 100, default = 'default')
    
    

# Create your models here.
